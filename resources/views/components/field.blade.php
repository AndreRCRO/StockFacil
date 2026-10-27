@props(['name', 'label', 'hint' => null])
<div {{ $attributes->class(['field']) }}>
    <label for="{{ $name }}">{{ $label }}</label>
    {{ $slot }}
    @if($hint)<p class="field-hint" id="{{ $name }}-hint">{{ $hint }}</p>@endif
    @error($name)<p class="field-error" id="{{ $name }}-error">{{ $message }}</p>@enderror
</div>
