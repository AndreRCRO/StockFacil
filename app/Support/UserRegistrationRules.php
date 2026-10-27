<?php

namespace App\Support;

use App\Models\User;
use Closure;

final class UserRegistrationRules
{
    public static function account(): array
    {
        return [
            'name' => ['required', 'string', 'max:120'],
            'email' => ['bail', 'required', 'string', 'email', 'max:255', function (string $attribute, mixed $value, Closure $fail): void {
                if (User::query()->whereRaw('LOWER(TRIM(email)) = ?', [$value])->exists()) {
                    $fail('Este correo electrónico ya está registrado.');
                }
            }],
            'password' => ['bail', 'required', 'string', 'min:8', function (string $attribute, mixed $value, Closure $fail): void {
                if (strlen($value) > 72) {
                    $fail('La contraseña no debe superar 72 bytes.');
                }
            }],
        ];
    }
}
