<?php

namespace App\Http\Requests;

use App\Models\Movement;
use App\Models\Product;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class MovementRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user() !== null;
    }

    public function rules(): array
    {
        return [
            'product_id' => ['required', 'integer', Rule::exists('products', 'id')->where('is_active', true)],
            'type' => ['required', Rule::in([Movement::ENTRY, Movement::EXIT])],
            'quantity' => ['required', 'integer', 'min:1', 'max:'.Product::MAX_STOCK],
            'note' => ['nullable', 'string', 'max:2000'],
        ];
    }

    public function attributes(): array
    {
        return ['product_id' => 'producto activo', 'type' => 'tipo', 'quantity' => 'cantidad', 'note' => 'observación'];
    }

    public function messages(): array
    {
        return [
            'quantity.min' => 'La cantidad debe ser mayor o igual a :min.',
            'quantity.max' => 'La cantidad no debe superar :max.',
        ];
    }
}
