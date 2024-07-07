Theorem deMorgan1: forall A B:Prop, ~(A\/B) -> ~A/\~B.
Proof.
    intros A B NAB.
    split.

    (* NAB: ~(A\/B) |- ~A *)
    - intro A1.
      apply NAB.
      left.
      exact A1.

    (* NAB: ~(A\/B) |- ~B *)
    - intro B1.
    apply NAB.
    right.
    exact B1.
Qed.

Print deMorgan1.
