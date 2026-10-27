<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware): void {
        //
    })
    ->withExceptions(function (Exceptions $exceptions): void {
        $exceptions->render(function (ValidationException $exception, Request $request) {
            if ($request->expectsJson()) {
                return null;
            }

            // Forms contain scalar fields. Do not echo malformed arrays into Blade inputs.
            $input = array_filter(
                $request->except(['password', 'password_confirmation', 'current_password']),
                fn ($value) => is_scalar($value) || $value === null,
            );

            return back()->withErrors($exception->errors(), $exception->errorBag)->withInput($input);
        });
    })->create();
