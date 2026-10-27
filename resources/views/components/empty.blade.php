@props(['title', 'text'])
<div class="empty-state"><x-icon name="box" size="28"/><h3>{{ $title }}</h3><p>{{ $text }}</p>{{ $slot }}</div>
