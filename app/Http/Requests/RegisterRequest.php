<?php

namespace App\Http\Requests;

use App\Support\EmailNormalizer;
use App\Support\UserRegistrationRules;
use Illuminate\Foundation\Http\FormRequest;

class RegisterRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    protected function prepareForValidation(): void
    {
        if (is_string($this->input('email'))) {
            $this->merge(['email' => EmailNormalizer::normalize($this->input('email'))]);
        }
    }

    public function rules(): array
    {
        $rules = UserRegistrationRules::account();
        array_splice($rules['password'], 4, 0, ['confirmed']);

        return $rules;
    }

    public function attributes(): array
    {
        return ['name' => 'nombre', 'email' => 'correo electrónico', 'password' => 'contraseña'];
    }

    public function messages(): array
    {
        return ['email.unique' => 'Este correo electrónico ya está registrado.', 'password.min' => 'La contraseña debe tener al menos 8 caracteres.', 'password.confirmed' => 'La confirmación de la contraseña no coincide.'];
    }
}
