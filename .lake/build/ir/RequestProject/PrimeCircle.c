// Lean compiler output
// Module: RequestProject.PrimeCircle
// Imports: public import Init public import Mathlib
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* lean_nat_gcd(lean_object*, lean_object*);
lean_object* lp_mathlib_Multiset_filter___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_fareyNew___lam__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0(lean_object*, lean_object*);
lean_object* lp_mathlib_Finset_map___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_fareyNew(lean_object*);
lean_object* l_List_range(lean_object*);
LEAN_EXPORT uint8_t lp_RequestProject_fareyNew___lam__1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_List_filterTR_loop___at___00Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0_spec__1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_Finset_filter___at___00fareySet_spec__0___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_fareySet(lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lp_mathlib_Multiset_product___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_fareyNew___lam__1___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_Finset_filter___at___00fareySet_spec__0(lean_object*, lean_object*);
lean_object* l_List_reverse___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_fareySet___boxed(lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_RequestProject_List_filterTR_loop___at___00Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0_spec__1(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_3; 
x_3 = l_List_reverse___redArg(x_2);
return x_3;
}
else
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_1);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; uint8_t x_10; 
x_5 = lean_ctor_get(x_1, 0);
x_6 = lean_ctor_get(x_1, 1);
x_7 = lean_ctor_get(x_5, 0);
x_8 = lean_ctor_get(x_5, 1);
x_9 = lean_unsigned_to_nat(1u);
x_10 = lean_nat_dec_le(x_9, x_8);
if (x_10 == 0)
{
lean_free_object(x_1);
lean_dec(x_5);
x_1 = x_6;
goto _start;
}
else
{
uint8_t x_12; 
x_12 = lean_nat_dec_le(x_7, x_8);
if (x_12 == 0)
{
lean_free_object(x_1);
lean_dec(x_5);
x_1 = x_6;
goto _start;
}
else
{
lean_object* x_14; uint8_t x_15; 
x_14 = lean_nat_gcd(x_7, x_8);
x_15 = lean_nat_dec_eq(x_14, x_9);
lean_dec(x_14);
if (x_15 == 0)
{
lean_free_object(x_1);
lean_dec(x_5);
x_1 = x_6;
goto _start;
}
else
{
lean_ctor_set(x_1, 1, x_2);
{
lean_object* _tmp_0 = x_6;
lean_object* _tmp_1 = x_1;
x_1 = _tmp_0;
x_2 = _tmp_1;
}
goto _start;
}
}
}
}
else
{
lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; uint8_t x_23; 
x_18 = lean_ctor_get(x_1, 0);
x_19 = lean_ctor_get(x_1, 1);
lean_inc(x_19);
lean_inc(x_18);
lean_dec(x_1);
x_20 = lean_ctor_get(x_18, 0);
x_21 = lean_ctor_get(x_18, 1);
x_22 = lean_unsigned_to_nat(1u);
x_23 = lean_nat_dec_le(x_22, x_21);
if (x_23 == 0)
{
lean_dec(x_18);
x_1 = x_19;
goto _start;
}
else
{
uint8_t x_25; 
x_25 = lean_nat_dec_le(x_20, x_21);
if (x_25 == 0)
{
lean_dec(x_18);
x_1 = x_19;
goto _start;
}
else
{
lean_object* x_27; uint8_t x_28; 
x_27 = lean_nat_gcd(x_20, x_21);
x_28 = lean_nat_dec_eq(x_27, x_22);
lean_dec(x_27);
if (x_28 == 0)
{
lean_dec(x_18);
x_1 = x_19;
goto _start;
}
else
{
lean_object* x_30; 
x_30 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_30, 0, x_18);
lean_ctor_set(x_30, 1, x_2);
x_1 = x_19;
x_2 = x_30;
goto _start;
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_RequestProject_Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0___redArg(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; 
x_2 = lean_box(0);
x_3 = lp_RequestProject_List_filterTR_loop___at___00Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0_spec__1(x_1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_RequestProject_fareySet(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_2 = lean_unsigned_to_nat(1u);
x_3 = lean_nat_add(x_1, x_2);
x_4 = l_List_range(x_3);
lean_inc(x_4);
x_5 = lp_mathlib_Multiset_product___redArg(x_4, x_4);
x_6 = lp_RequestProject_Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0___redArg(x_5);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_RequestProject_fareySet___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lp_RequestProject_fareySet(x_1);
lean_dec(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_RequestProject_Finset_filter___at___00fareySet_spec__0___redArg(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lp_RequestProject_Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0___redArg(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_RequestProject_Finset_filter___at___00fareySet_spec__0(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_RequestProject_Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0___redArg(x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_RequestProject_Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_RequestProject_Multiset_filter___at___00Finset_filter___at___00fareySet_spec__0_spec__0___redArg(x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_RequestProject_fareyNew___lam__0(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
LEAN_EXPORT uint8_t lp_RequestProject_fareyNew___lam__1(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; lean_object* x_4; uint8_t x_5; 
x_3 = lean_nat_gcd(x_2, x_1);
x_4 = lean_unsigned_to_nat(1u);
x_5 = lean_nat_dec_eq(x_3, x_4);
lean_dec(x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_RequestProject_fareyNew___lam__1___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_3; lean_object* x_4; 
x_3 = lp_RequestProject_fareyNew___lam__1(x_1, x_2);
lean_dec(x_2);
lean_dec(x_1);
x_4 = lean_box(x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_RequestProject_fareyNew(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; 
lean_inc(x_1);
x_2 = lean_alloc_closure((void*)(lp_RequestProject_fareyNew___lam__0), 2, 1);
lean_closure_set(x_2, 0, x_1);
lean_inc(x_1);
x_3 = lean_alloc_closure((void*)(lp_RequestProject_fareyNew___lam__1___boxed), 2, 1);
lean_closure_set(x_3, 0, x_1);
x_4 = l_List_range(x_1);
x_5 = lp_mathlib_Multiset_filter___redArg(x_3, x_4);
x_6 = lp_mathlib_Finset_map___redArg(x_2, x_5);
return x_6;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_RequestProject_RequestProject_PrimeCircle(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
