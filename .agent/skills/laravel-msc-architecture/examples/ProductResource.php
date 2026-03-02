<?php

namespace App\Http\Resources\Product;

use App\Helpers\DateHelper;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ProductResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'sku' => $this->sku,
            'price' => (float) $this->price,
            'stock' => $this->stock_quantity,
            'is_active' => $this->is_active,
            // Standardized Dates
            'created_at' => DateHelper::formatDateTime($this->created_at),
            'updated_at' => DateHelper::formatDateTime($this->updated_at),
        ];
    }
}