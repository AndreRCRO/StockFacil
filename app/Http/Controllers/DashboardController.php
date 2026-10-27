<?php

namespace App\Http\Controllers;

use App\Models\Movement;
use App\Models\Product;
use Illuminate\View\View;

class DashboardController extends Controller
{
    public function __invoke(): View
    {
        return view('dashboard', [
            'totalProducts' => Product::active()->count(), 'totalUnits' => (int) Product::active()->sum('stock'),
            'lowStockCount' => Product::lowStock()->count(), 'outOfStockCount' => Product::active()->where('stock', 0)->count(),
            'alerts' => Product::lowStock()->with('category')->orderBy('stock')->orderBy('name')->limit(4)->get(),
            'recentMovements' => Movement::with(['product', 'user'])->latest('id')->limit(5)->get(),
        ]);
    }
}
