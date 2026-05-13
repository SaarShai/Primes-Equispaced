/-
Register the `@[category]` and `@[AMS]` tag attributes used by
google-deepmind/formal-conjectures.  These are no-op tags that carry
metadata only; they have no effect on elaboration or code generation.
-/
import Lean

open Lean in
initialize _categoryAttr : TagAttribute ←
  registerTagAttribute `category "Formal-conjectures category tag (no-op)"

open Lean in
initialize _amsAttr : TagAttribute ←
  registerTagAttribute `AMS "AMS classification tag (no-op)"
