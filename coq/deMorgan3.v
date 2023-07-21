Theorem deMorgan3: forall A B:Prop, ~A\/~B -> ~(A/\B).
Proof.
    intros A B NANB AB.
    destruct AB as [A1 B1].
    destruct NANB as [NA | NB].

    (* A1: A, B1: B, NA:~A |- False*)
    - apply NA.
      exact A1.
    (* A1: A, B1: B, NA:~B |- False*)
    - apply NB.
      exact B1.
Qed.

Print deMorgan3.