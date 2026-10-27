@if(session('status'))
    <div class="flash flash-success" role="status"><x-icon name="check"/>{{ session('status') }}</div>
@endif
@if($errors->any())
    <div class="flash flash-error" role="alert"><x-icon name="alert"/><div><strong>Revisa los datos antes de guardar.</strong><ul>@foreach($errors->all() as $message)<li>{{ $message }}</li>@endforeach</ul></div></div>
@endif
