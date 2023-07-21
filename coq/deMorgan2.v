Theorem deMorgan2: forall A B:Prop, ~A/\~B -> ~(A\/B).
Proof.
    intros A B NANB AB.
    destruct NANB as [NA NB].
    destruct AB as [A1 | B1].

    (* NA:~A, NB: ~B A1:A |- False *)
    - apply NA.
      exact A1.

    (* NA:~A, NB:~B B1:B |- False*)
    - apply NB.
      exact B1.
Qed.

Print deMorgan2.