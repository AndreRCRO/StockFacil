<?php

namespace App\Http\Controllers;

use App\Domain\Users\RegistrationData;
use App\Http\Requests\RegisterRequest;
use App\Services\RegisterUser;
use Illuminate\Http\RedirectResponse;
use Illuminate\View\View;

class RegistrationController extends Controller
{
    public function create(): View
    {
        return view('auth.register');
    }

    public function store(RegisterRequest $request, RegisterUser $registration): RedirectResponse
    {
        $registration->register(new RegistrationData(...$request->safe()->only(['name', 'email', 'password'])));

        return redirect()->route('login')->with('status', 'Cuenta creada correctamente. Ya puedes iniciar sesión.');
    }
}
