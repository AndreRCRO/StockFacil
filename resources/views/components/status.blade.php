@props(['product'])
@php($tone = ! $product->is_active ? 'neutral' : ($product->stock === 0 ? 'danger' : ($product->stock <= $product->minimum_stock ? 'warning' : 'success')))
<span class="badge badge-{{ $tone }}"><span class="status-dot"></span>{{ $product->is_active ? $product->stock_status : 'Inactivo' }}</span>
