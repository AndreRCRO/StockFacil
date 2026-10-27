<?php

namespace App\Http\Requests;

use App\Models\Product;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class ProductRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user() !== null;
    }

    protected function prepareForValidation(): void
    {
        if (is_string($this->input('sku'))) {
            $this->merge(['sku' => mb_strtoupper(trim($this->input('sku')))]);
        }
    }

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:150'],
            'sku' => ['required', 'string', 'max:60', Rule::unique('products')->ignore($this->route('product'))],
            'category_id' => ['required', 'integer', 'exists:categories,id'],
            'description' => ['nullable', 'string', 'max:2000'],
            'price' => ['required', 'numeric', 'min:0', 'max:9999999999.99', 'decimal:0,2'],
            'minimum_stock' => ['required', 'integer', 'min:0', 'max:'.Product::MAX_STOCK],
            'initial_stock' => $this->isMethod('POST') ? ['required', 'integer', 'min:0', 'max:'.Product::MAX_STOCK] : ['prohibited'],
            'stock' => ['prohibited'], 'is_active' => ['prohibited'],
        ];
    }

    public function attributes(): array
    {
        return ['name' => 'nombre', 'sku' => 'SKU', 'category_id' => 'categoría', 'price' => 'precio', 'minimum_stock' => 'stock mínimo', 'initial_stock' => 'stock inicial', 'description' => 'descripción'];
    }
}
