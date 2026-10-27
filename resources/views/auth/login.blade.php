<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#234e43"><title>Iniciar sesión · StockFácil</title>@vite(['resources/css/app.css', 'resources/js/app.js'])</head>
<body class="login-body">
    <main class="login-shell">
        <section class="login-story">
            <a class="brand" href="{{ route('login') }}"><span class="brand-symbol"><x-icon name="box" size="25"/></span><span>Stock<span class="brand-light">Fácil</span></span></a>
            <div class="login-message"><h1>Un negocio en movimiento.<br><span>Un inventario en orden.</span></h1><p>Conoce lo que tienes, registra lo que cambia y repón a tiempo.</p></div>
            <div class="login-features"><div><x-icon name="box"/><span>Todos tus productos en un lugar.</span></div><div><x-icon name="arrows"/><span>Cada entrada y salida, registrada.</span></div><div><x-icon name="alert"/><span>Stock bajo siempre a la vista.</span></div></div>
            <p class="login-story-footer">Hecho para el día a día de tu negocio.</p>
        </section>
        <section class="login-panel" aria-labelledby="login-heading">
            <div class="login-form-wrap"><h2 id="login-heading">Bienvenido de nuevo</h2><p class="lead">Ingresa para administrar tu inventario.</p><x-flash/>
                <form action="{{ route('login.store') }}" method="POST" data-submit-form>
                    @csrf
                    <x-field name="email" label="Correo electrónico"><input id="email" name="email" type="email" value="{{ old('email') }}" autocomplete="username" required autofocus aria-invalid="{{ $errors->has('email') ? 'true' : 'false' }}" @error('email') aria-describedby="email-error" @enderror></x-field>
                    <x-field name="password" label="Contraseña"><input id="password" name="password" type="password" autocomplete="current-password" required aria-invalid="{{ $errors->has('password') ? 'true' : 'false' }}" @error('password') aria-describedby="password-error" @enderror></x-field>
                    <button type="submit" class="btn btn-primary w-full" data-loading-text="Ingresando…">Iniciar sesión<x-icon name="right"/></button>
                </form>
                <p class="login-note">¿Aún no tienes cuenta? <a href="{{ route('register') }}">Crear cuenta</a></p>
            </div>
        </section>
    </main>
</body>
</html>
