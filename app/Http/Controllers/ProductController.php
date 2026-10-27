<?php

namespace App\Http\Controllers;

use App\Http\Requests\ProductRequest;
use App\Models\Category;
use App\Models\Product;
use App\Services\InventoryService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Validation\Rule;
use Illuminate\View\View;

class ProductController extends Controller
{
    public function index(Request $request): View
    {
        $filters = $request->validate(['q' => ['nullable', 'string', 'max:150'], 'category_id' => ['nullable', 'integer', 'exists:categories,id'], 'status' => ['nullable', Rule::in(['active', 'inactive', 'all'])]]);
        $query = Product::with('category');
        $status = $filters['status'] ?? 'active';
        if ($status !== 'all') {
            $query->where('is_active', $status === 'active');
        }
        if ($search = $filters['q'] ?? null) {
            $query->where(fn ($query) => $query->where('name', 'like', '%'.$search.'%')->orWhere('sku', 'like', '%'.$search.'%'));
        }
        $query->when($filters['category_id'] ?? null, fn ($query, $id) => $query->where('category_id', $id));

        return view('products.index', ['products' => $query->orderBy('name')->paginate(10)->withQueryString(), 'categories' => Category::orderBy('name')->get()]);
    }

    public function create(): View
    {
        return view('products.form', ['product' => new Product, 'categories' => Category::orderBy('name')->get()]);
    }

    public function store(ProductRequest $request, InventoryService $inventory): RedirectResponse
    {
        $inventory->createProduct($request->validated(), $request->user());

        return redirect()->route('products.index')->with('status', 'Producto registrado. El stock inicial quedó en el historial.');
    }

    public function edit(Product $product): View
    {
        return view('products.form', ['product' => $product, 'categories' => Category::orderBy('name')->get()]);
    }

    public function update(ProductRequest $request, Product $product): RedirectResponse
    {
        $product->update($request->validated());

        return redirect()->route('products.index', ['status' => $product->is_active ? 'active' : 'inactive'])->with('status', 'Datos del producto actualizados.');
    }

    public function deactivate(Product $product): RedirectResponse
    {
        $product->update(['is_active' => false]);

        return redirect()->route('products.index')->with('status', 'Producto desactivado. Su historial se conserva.');
    }

    public function lowStock(Request $request): View
    {
        $request->validate(['q' => ['nullable', 'string', 'max:150']]);
        $query = Product::lowStock()->with('category');
        if ($search = $request->input('q')) {
            $query->where(fn ($query) => $query->where('name', 'like', '%'.$search.'%')->orWhere('sku', 'like', '%'.$search.'%'));
        }

        return view('products.low-stock', ['products' => $query->orderBy('stock')->orderBy('name')->paginate(10)->withQueryString()]);
    }
}
