@props(['title' => 'Dashboard'])
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#234e43">
    <title>{{ $title }} · StockFácil</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <a class="skip-link" href="#main-content">Ir al contenido</a>
    <div class="app-shell">
        <div class="sidebar-overlay" data-menu-overlay hidden></div>
        <aside class="sidebar" id="sidebar" aria-label="Menú principal">
            <a class="brand" href="{{ route('dashboard') }}"><span class="brand-symbol"><x-icon name="box" size="25"/></span><span>Stock<span class="brand-light">Fácil</span><small>Tu inventario, en orden.</small></span></a>
            <button type="button" class="mobile-close icon-button" data-menu-close aria-label="Cerrar menú"><x-icon name="close"/></button>
            <nav>
                @foreach([['dashboard', 'grid', 'Dashboard'], ['products.index', 'box', 'Productos'], ['movements.index', 'arrows', 'Movimientos'], ['products.low-stock', 'alert', 'Stock bajo']] as [$route, $icon, $label])
                    @php($active = $route === 'products.index' ? request()->routeIs('products.*') && !request()->routeIs('products.low-stock') : ($route === 'movements.index' ? request()->routeIs('movements.*') : request()->routeIs($route)))
                    <a href="{{ route($route) }}" class="nav-link {{ $active ? 'active' : '' }}" @if($active) aria-current="page" @endif><x-icon :name="$icon"/>{{ $label }}@if($active)<span class="nav-dot"></span>@endif</a>
                @endforeach
            </nav>
            <div class="sidebar-bottom">
                <div class="user-block"><span class="avatar">{{ mb_substr(auth()->user()->name, 0, 1) }}</span><div><strong>{{ auth()->user()->name }}</strong><small>Administrador</small></div></div>
                <form action="{{ route('logout') }}" method="POST">@csrf<button class="nav-link logout" type="submit"><x-icon name="logout"/>Cerrar sesión</button></form>
            </div>
        </aside>
        <div class="main-area">
            <header class="topbar"><div class="topbar-left"><button class="icon-button menu-toggle" type="button" data-menu-toggle aria-controls="sidebar" aria-expanded="false" aria-label="Abrir menú"><x-icon name="menu"/></button><span>Mi negocio</span><span class="topbar-slash">/</span><strong>{{ $title }}</strong></div><span class="topbar-date">{{ now()->translatedFormat('d M Y') }}</span></header>
            <main id="main-content" tabindex="-1"><x-flash/>{{ $slot }}</main>
            <footer class="app-footer"><span>StockFácil</span><span>Un movimiento a la vez, todo bajo control.</span></footer>
        </div>
    </div>
</body>
</html>
