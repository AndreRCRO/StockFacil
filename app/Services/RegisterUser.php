<?php

namespace App\Services;

use App\Domain\Users\RegistrationData;
use App\Models\User;
use App\Support\UserRegistrationRules;
use Illuminate\Database\UniqueConstraintViolationException;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\ValidationException;

class RegisterUser
{
    public function register(RegistrationData $data): User
    {
        Validator::make(
            ['name' => $data->name, 'email' => $data->email, 'password' => $data->password],
            UserRegistrationRules::account(),
        )->validate();

        try {
            return User::create(['name' => $data->name, 'email' => $data->email, 'password' => $data->password]);
        } catch (UniqueConstraintViolationException) {
            throw ValidationException::withMessages(['email' => 'Este correo electrónico ya está registrado.']);
        }
    }
}
