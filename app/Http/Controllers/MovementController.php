<?php

namespace App\Http\Controllers;

use App\Http\Requests\MovementRequest;
use App\Models\Movement;
use App\Models\Product;
use App\Services\InventoryService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Validation\Rule;
use Illuminate\View\View;

class MovementController extends Controller
{
    public function index(Request $request): View
    {
        $filters = $request->validate(['product_id' => ['nullable', 'integer', 'exists:products,id'], 'type' => ['nullable', Rule::in([Movement::ENTRY, Movement::EXIT])]]);
        $movements = Movement::with(['product', 'user'])
            ->when($filters['product_id'] ?? null, fn ($query, $id) => $query->where('product_id', $id))
            ->when($filters['type'] ?? null, fn ($query, $type) => $query->where('type', $type))
            ->latest('id')->paginate(10)->withQueryString();

        return view('movements.index', ['movements' => $movements, 'products' => Product::orderBy('name')->get()]);
    }

    public function create(Request $request): View
    {
        $request->validate(['product_id' => ['nullable', 'integer', 'exists:products,id'], 'type' => ['nullable', Rule::in([Movement::ENTRY, Movement::EXIT])]]);

        return view('movements.form', ['products' => Product::active()->orderBy('name')->get()]);
    }

    public function store(MovementRequest $request, InventoryService $inventory): RedirectResponse
    {
        $data = $request->validated();
        $inventory->record(Product::findOrFail($data['product_id']), $data['type'], (int) $data['quantity'], $request->user(), $data['note'] ?? null);

        return redirect()->route('movements.index')->with('status', 'Movimiento registrado y existencias actualizadas.');
    }
}
