<?php

namespace App\Services\Product;

use App\Models\Product;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class ProductService
{
    /**
     * Create a new product with business logic (e.g. inventory checks)
     */
    public function createProduct(array $data): Product
    {
        return DB::transaction(function () use ($data) {
            // Example logic: Auto-activate if stock > 0
            if (isset($data['stock_quantity']) && $data['stock_quantity'] > 0) {
                $data['is_active'] = true;
            }

            $product = Product::create($data);

            Log::info("Product created: {$product->sku}");

            return $product;
        });
    }

    /**
     * Update product logic
     */
    public function updateProduct(Product $product, array $data): Product
    {
        return DB::transaction(function () use ($product, $data) {
            $product->update($data);
            return $product->refresh();
        });
    }
}