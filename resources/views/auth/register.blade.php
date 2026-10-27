<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#234e43"><title>Crear cuenta · StockFácil</title>@vite(['resources/css/app.css', 'resources/js/app.js'])</head>
<body class="login-body">
    <main class="login-shell">
        <section class="login-story">
            <a class="brand" href="{{ route('login') }}"><span class="brand-symbol"><x-icon name="box" size="25"/></span><span>Stock<span class="brand-light">Fácil</span></span></a>
            <div class="login-message"><h1>Tu inventario comienza<br><span>con una cuenta.</span></h1><p>Registra tus datos para acceder a StockFácil.</p></div>
            <div class="login-features"><div><x-icon name="box"/><span>Todos tus productos en un lugar.</span></div><div><x-icon name="arrows"/><span>Cada entrada y salida, registrada.</span></div><div><x-icon name="alert"/><span>Stock bajo siempre a la vista.</span></div></div>
            <p class="login-story-footer">Hecho para el día a día de tu negocio.</p>
        </section>
        <section class="login-panel" aria-labelledby="register-heading">
            <div class="login-form-wrap"><h2 id="register-heading">Crear cuenta</h2><p class="lead">Completa tus datos para comenzar.</p><x-flash/>
                <form action="{{ route('register.store') }}" method="POST" data-submit-form>
                    @csrf
                    <x-field name="name" label="Nombre"><input id="name" name="name" value="{{ old('name') }}" maxlength="120" autocomplete="name" required autofocus aria-invalid="{{ $errors->has('name') ? 'true' : 'false' }}" @error('name') aria-describedby="name-error" @enderror></x-field>
                    <x-field name="email" label="Correo electrónico"><input id="email" name="email" type="email" value="{{ old('email') }}" maxlength="255" autocomplete="email" required aria-invalid="{{ $errors->has('email') ? 'true' : 'false' }}" @error('email') aria-describedby="email-error" @enderror></x-field>
                    <x-field name="password" label="Contraseña" hint="Usa al menos 8 caracteres y como máximo 72 bytes."><input id="password" name="password" type="password" minlength="8" autocomplete="new-password" required aria-invalid="{{ $errors->has('password') ? 'true' : 'false' }}" aria-describedby="password-hint{{ $errors->has('password') ? ' password-error' : '' }}"></x-field>
                    <x-field name="password_confirmation" label="Confirmar contraseña"><input id="password_confirmation" name="password_confirmation" type="password" autocomplete="new-password" required></x-field>
                    <button type="submit" class="btn btn-primary w-full" data-loading-text="Creando cuenta…">Crear cuenta<x-icon name="right"/></button>
                </form>
                <p class="login-note">¿Ya tienes cuenta? <a href="{{ route('login') }}">Iniciar sesión</a></p>
            </div>
        </section>
    </main>
</body>
</html>
