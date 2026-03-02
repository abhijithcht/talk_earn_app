<?php

namespace App\Http\Controllers\Api;

use App\Helpers\PaginationHelper;
use App\Helpers\ResponseHelper;
use App\Http\Controllers\Controller;
use App\Http\Requests\Product\StoreProductRequest;
use App\Http\Requests\Product\UpdateProductRequest;
use App\Http\Resources\Product\ProductResource;
use App\Models\Product;
use App\Services\Product\ProductService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Throwable;

class ProductController extends Controller
{
    public function __construct(
        protected ProductService $service
    ) {}

    public function index(Request $request): JsonResponse
    {
        $this->authorize('viewAny', Product::class);

        $query = Product::query();

        // Searchable fields defined here for PaginationHelper
        $searchFields = ['name', 'sku', 'description'];

        $paginatedData = PaginationHelper::paginate($query, $request, $searchFields);

        // Wrap items in Resource
        $paginatedData->setCollection(
            ProductResource::collection($paginatedData->getCollection())->collection
        );

        return ResponseHelper::paginated($paginatedData);
    }

    public function store(StoreProductRequest $request): JsonResponse
    {
        $this->authorize('create', Product::class);

        try {
            $product = $this->service->createProduct($request->validated());

            return ResponseHelper::created(
                new ProductResource($product),
                'Product created successfully.'
            );
        } catch (Throwable $e) {
            ResponseHelper::logError('Failed to create product', $e);
            return ResponseHelper::error('Unable to create product.', 500);
        }
    }

    public function show(Product $product): JsonResponse
    {
        $this->authorize('view', $product);

        return ResponseHelper::success(
            'Product retrieved.',
            new ProductResource($product)
        );
    }
}