---
id: skill_laravel_pest
name: Laravel Pest Architect
version: 3.0.0
description: Pure Pest PHP testing conventions for Laravel applications. Generates high-performance tests using SQLite in-memory databases with functional Pest syntax.
tags: [laravel, testing, pest, tdd, php]
permissions: [read_code, write_file, execute_terminal]
---

# Laravel Pest Testing Guide

## 1. Directory Structure

Tests mirror the `app/` folder structure for discoverability.

| Source (`app/`)                           | Test (`tests/`)                           | Type    |
| :---------------------------------------- | :---------------------------------------- | :------ |
| `Http/Controllers/Api/UserController.php` | `Feature/Api/UserTest.php`                | Feature |
| `Http/Controllers/Web/PostController.php` | `Feature/Web/PostTest.php`                | Feature |
| `Services/PaymentService.php`             | `Feature/Services/PaymentServiceTest.php` | Feature |
| `Policies/PostPolicy.php`                 | `Feature/PostPolicyTest.php`              | Feature |
| `Mail/WelcomeMail.php`                    | `Feature/Mail/WelcomeMailTest.php`        | Feature |

> **Note:** Service tests are placed in `Feature/` (not `Unit/`) when they interact with the database.

---

## 2. Configuration

### Global Setup (`tests/Pest.php`)
```php
pest()->extend(Tests\TestCase::class)
    ->use(Illuminate\Foundation\Testing\RefreshDatabase::class)
    ->in('Feature');
```

- `RefreshDatabase` is applied **globally** to all Feature tests
- Individual test files do NOT need `uses(RefreshDatabase::class)`
- Unit tests (in `tests/Unit/`) do not use database traits

### PHPUnit Configuration (`phpunit.xml`)
```xml
<env name="DB_CONNECTION" value="sqlite"/>
<env name="DB_DATABASE" value=":memory:"/>
```

---

## 3. Test Syntax

All tests use Pest functional style with `it()` syntax.

```php
<?php

use App\Models\User;

it('user can register', function () {
    $response = $this->postJson('/api/register', [
        'name' => 'Test User',
        'email' => 'test@example.com',
        'password' => 'password123',
    ]);

    $response->assertCreated()
        ->assertJsonStructure(['success', 'message', 'data']);
});
```

### Test Grouping with `describe()`
```php
describe('authentication', function () {
    it('allows login with valid credentials', function () {
        // ...
    });

    it('rejects login with invalid credentials', function () {
        // ...
    });
});
```

---

## 4. Assertion Strategy

| Context        | Use This           | Example                                                              |
| :------------- | :----------------- | :------------------------------------------------------------------- |
| HTTP Response  | Laravel fluent API | `$response->assertOk()->assertJsonPath('data.name', 'John')`         |
| JSON Structure | Laravel assertJson | `$response->assertJsonStructure(['success', 'data' => ['id']])`      |
| Value Checks   | Pest `expect()`    | `expect($user->is_active)->toBeTrue()`                               |
| Database State | Laravel assertions | `$this->assertDatabaseHas('users', ['email' => 'test@example.com'])` |
| Soft Deletes   | Laravel assertions | `$this->assertSoftDeleted($model)`                                   |

### Common Patterns

**API Success Response:**
```php
$response->assertCreated()
    ->assertJson([
        'success' => true,
        'message' => 'Created successfully',
    ])
    ->assertJsonPath('data.name', 'John Doe');
```

**Chained Expectations:**
```php
expect($user)
    ->is_active->toBeTrue()
    ->email->toBe('test@example.com');
```

**Higher-Order Expectations:**
```php
expect($users)
    ->toHaveCount(3)
    ->each->toBeInstanceOf(User::class);
```

---

## 5. Test Setup Patterns

### Service Tests: Use `beforeEach()`
```php
<?php

use App\Services\PaymentService;

beforeEach(function () {
    $this->service = new PaymentService;
});

it('can process payment', function () {
    $result = $this->service->charge(100);
    expect($result)->toBeTrue();
});
```

### Shared Setup with `beforeEach()`
```php
<?php

use App\Models\User;

beforeEach(function () {
    $this->user = User::factory()->create();
});

it('can list posts', function () {
    $response = $this->actingAs($this->user)
        ->getJson('/api/posts');

    $response->assertOk();
});

it('can create post', function () {
    $response = $this->actingAs($this->user)
        ->postJson('/api/posts', ['title' => 'My Post']);

    $response->assertCreated();
});
```

---

## 6. Mocking & Fakes

### Facade Fakes
```php
it('sends welcome email', function () {
    Mail::fake();

    $this->postJson('/api/register', [...]);

    Mail::assertQueued(WelcomeMail::class);
});
```

### Service Mocking
```php
it('mocks external API', function () {
    $mock = mock(ExternalApiService::class)
        ->shouldReceive('sync')
        ->once()
        ->andReturn(true)
        ->getMock();

    app()->instance(ExternalApiService::class, $mock);

    // Test code that uses the service
});
```

### Partial Mocks
```php
it('partially mocks a service', function () {
    $service = mock(PaymentService::class)->makePartial();
    $service->shouldReceive('charge')->andReturn(true);

    expect($service->process())->toBeTrue();
});
```

---

## 7. Architecture Tests

Location: `tests/Feature/ArchTest.php`

```php
<?php

arch('globals')
    ->expect(['dd', 'dump', 'ray', 'env'])
    ->not->toBeUsed();

arch('controllers')
    ->expect('App\Http\Controllers')
    ->not->toUse('Illuminate\Support\Facades\Validator');

arch('models')
    ->expect('App\Models')
    ->toExtend('Illuminate\Database\Eloquent\Model');

arch('models should not depend on request')
    ->expect('App\Models')
    ->not->toUse('Illuminate\Http\Request');

arch('resources extend JsonResource')
    ->expect('App\Http\Resources')
    ->toExtend('Illuminate\Http\Resources\Json\JsonResource');

arch('services are classes')
    ->expect('App\Services')
    ->toBeClasses();
```

---

## 8. Datasets

### Inline Datasets
```php
it('validates email format', function (string $email, bool $valid) {
    $response = $this->postJson('/api/register', [
        'email' => $email,
        'name' => 'Test',
        'password' => 'password123',
    ]);

    if ($valid) {
        $response->assertCreated();
    } else {
        $response->assertUnprocessable();
    }
})->with([
    ['test@example.com', true],
    ['invalid-email', false],
    ['test@', false],
]);
```

### Named Datasets
```php
dataset('invalid_emails', [
    'missing @' => ['invalidemail.com'],
    'missing domain' => ['test@'],
    'spaces' => ['test @example.com'],
]);

it('rejects invalid emails', function (string $email) {
    $response = $this->postJson('/api/register', [
        'email' => $email,
        'name' => 'Test',
        'password' => 'password123',
    ]);

    $response->assertUnprocessable();
})->with('invalid_emails');
```

---

## 9. Scaffold Templates

### Feature Controller Test
**Trigger:** `/test gen Http/Controllers/PostController`

```php
<?php

use App\Models\User;
use App\Models\Post;

beforeEach(function () {
    $this->user = User::factory()->create();
});

it('can list posts', function () {
    Post::factory()->for($this->user)->create();

    $response = $this->actingAs($this->user)
        ->getJson('/api/posts');

    $response->assertOk()
        ->assertJsonStructure(['data']);
});

it('can create post', function () {
    $response = $this->actingAs($this->user)
        ->postJson('/api/posts', [
            'title' => 'My Post',
            'body' => 'Content here',
        ]);

    $response->assertCreated()
        ->assertJsonPath('data.title', 'My Post');

    $this->assertDatabaseHas('posts', ['title' => 'My Post']);
});

it('can show post', function () {
    $post = Post::factory()->for($this->user)->create();

    $response = $this->actingAs($this->user)
        ->getJson("/api/posts/{$post->id}");

    $response->assertOk()
        ->assertJsonPath('data.id', $post->id);
});

it('can update post', function () {
    $post = Post::factory()->for($this->user)->create();

    $response = $this->actingAs($this->user)
        ->putJson("/api/posts/{$post->id}", [
            'title' => 'Updated Title',
        ]);

    $response->assertOk()
        ->assertJsonPath('data.title', 'Updated Title');
});

it('can delete post', function () {
    $post = Post::factory()->for($this->user)->create();

    $response = $this->actingAs($this->user)
        ->deleteJson("/api/posts/{$post->id}");

    $response->assertOk();
    $this->assertSoftDeleted($post);
});
```

### Service Test
**Trigger:** `/test gen Services/PaymentService`

```php
<?php

use App\Models\User;
use App\Services\PaymentService;

beforeEach(function () {
    $this->service = new PaymentService;
});

it('can process payment', function () {
    $user = User::factory()->create();

    $result = $this->service->charge($user, 100);

    expect($result)
        ->status->toBe('completed')
        ->amount->toBe(100);

    $this->assertDatabaseHas('payments', [
        'user_id' => $user->id,
        'amount' => 100,
    ]);
});

it('throws exception for invalid amount', function () {
    $user = User::factory()->create();

    expect(fn () => $this->service->charge($user, -100))
        ->toThrow(InvalidArgumentException::class);
});
```

### Policy Test
**Trigger:** `/test gen Policies/PostPolicy`

```php
<?php

use App\Models\User;
use App\Models\Post;
use App\Policies\PostPolicy;

beforeEach(function () {
    $this->policy = new PostPolicy;
    $this->owner = User::factory()->create();
    $this->post = Post::factory()->for($this->owner, 'user')->create();
});

it('allows owner to update post', function () {
    expect($this->policy->update($this->owner, $this->post))->toBeTrue();
});

it('denies non-owner from updating post', function () {
    $otherUser = User::factory()->create();

    expect($this->policy->update($otherUser, $this->post))->toBeFalse();
});
```

---

## 10. Running Tests

```bash
# Run all tests (compact output)
php artisan test --compact

# Run specific file
php artisan test tests/Feature/Api/UserTest.php

# Filter by name
php artisan test --filter="user can login"

# Run only Feature tests
php artisan test --testsuite=Feature

# Run with coverage
php artisan test --coverage

# Run in parallel
php artisan test --parallel
```