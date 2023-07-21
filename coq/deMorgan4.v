Theorem deMorgan4: forall A B: Prop, ~(A/\B) -> ~A\/~B.
Proof.
    Require Import Classical.

    intros A B NAB.
    apply NNPP.
    intro NNANB.
    apply NAB.
    split.

    (* NNANB: ~(A\/~B) |- A*)
    - apply NNPP.
      intro NA.
      apply NNANB.
      left.
      exact NA.

    (* NNANB: ~(A\/~B) |- B*)
    - apply NNPP.
      intro NB.
      apply NNANB.
      right.
      exact NB.
Qed.

Print deMorgan4.