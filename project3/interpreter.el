;;; The store is simulated by an association list.  The key is the offset that
;;; has been allocated to an identifier in the AST.

(defun store (offset value alist)
  "Insert the value for this offset, replacing the previous value (if any)."
  (cond
   ((null alist)             (list (cons offset value)))    ; ((offset . value))
   ((eq offset (caar alist)) (cons (cons offset value) (cdr alist)))
   (t                        (cons (car alist)
                                   (store offset value (cdr alist))))
  )
)

(defun lookup (offset alist)
  "Return the value associated with this offset, or raise an error."
  (cond
   ((null alist)             (user-error "UNINITIALISED %s" offset) (exit))
   ((eq (caar alist) offset) (cdar alist))
   (t                        (lookup offset (cdr alist)))
  )
)

;; (setq a (store 1 19  (store 0 17 ())))
;; a
;; (setq a (store 2 20 a))
;; (setq a (store 1 29 a))
;; (lookup 3 ())
;; (lookup 3 a)
;; (lookup 1 a)


;;; Accessors for the various fields in an AST node

(defun kind (ast)
  "The kind of an AST node"
  " Your code goes here."
  (car ast)
)

(defun position (ast)
  "The position stored in an AST node"
  (cadr ast)
)

(defun operand (n ast)
  "The n'th operand of an AST node."
  " Your code goes here."
  (cond
   ((eq n 0) (caddr ast))
   ((eq n 1) (cadddr ast))
   ((eq n 2) (caddddr ast))
   ((null ast) (user-error "INTERNAL SERVICE ERROR") (exit))
  )
)

;; (setq ast '(OP_PLUS pos (VARIABLE pos b 1) (INT_LITERAL pos 77)))
;; (kind ast)
;; (position ast)
;; (kind (operand 0 ast))
;; (operand 1 ast)


;;; The interpreter itself.

;; exp must handle BOOL_LITERAL, INT_LITERAL, VARIABLE,
;;                 OP_PLUS, OP_MINUS, OP_MULT, OP_DIV,
;;                 OP_EQ, OP_NEQ, OP_LT, OP_LTE, OP_GT, OP_GTE,
;;                 OP_AND, OP_OR, OP_NOT

(defun exp (ast alist)
  "Evaluate an expression (given this alist to represent the variable store)."
  (cond
   ((eq (kind ast) 'BOOL_LITERAL) (eq (operand 0 ast) 'True))
   ((eq (kind ast) 'INT_LITERAL)  (operand 0 ast))
   ((eq (kind ast) 'VARIABLE)     (cond
				   ((eq (lookup (operand 1 ast) alist) 'True) t)
				   ((eq (lookup (operand 1 ast) alist) 'False) nil)
				   (t (lookup (operand 1 ast) alist))
				  ))
   ((eq (kind ast) 'OP_PLUS)      (+ (exp (operand 0 ast) alist) (exp (operand 1 ast) alist)))
   ((eq (kind ast) 'OP_MINUS)     (- (exp (operand 0 ast) alist) (exp (operand 1 ast) alist)))
   ((eq (kind ast) 'OP_MULT)      (* (exp (operand 0 ast) alist) (exp (operand 1 ast) alist)))
   ((eq (kind ast) 'OP_DIV)       (/ (exp (operand 0 ast) alist) (exp (operand 1 ast) alist))) 
   ((eq (kind ast) 'OP_EQ)        (eq (exp (operand 0 ast) alist) (exp (operand 1 ast) alist)))
   ((eq (kind ast) 'OP_NEQ)       (not (eq (exp (operand 0 ast) alist) (exp (operand 1 ast) alist))))
   ((eq (kind ast) 'OP_LT)        (< (exp (operand 0 ast) alist) (exp (operand 1 ast) alist)))
   ((eq (kind ast) 'OP_LTE)       (<= (exp (operand 0 ast) alist) (exp (operand 1 ast) alist)))
   ((eq (kind ast) 'OP_GT)        (> (exp (operand 0 ast) alist) (exp (operand 1 ast) alist)))
   ((eq (kind ast) 'OP_GTE)       (>= (exp (operand 0 ast) alist) (exp (operand 1 ast) alist)))
   ((eq (kind ast) 'OP_AND)       (and (exp (operand 0 ast) alist) (exp (operand 1 ast) alist)))
   ((eq (kind ast) 'OP_OR)        (or (exp (operand 0 ast) alist) (exp (operand 1 ast) alist)))
   ((eq (kind ast) 'OP_NOT)       (not (exp (operand 0 ast) alist)))
  )
)

;; (exp ast a)
;; (exp '(BOOL_LITERAL pos True) a)
;; (exp '(INT_LITERAL pos 45) a)


;; (setq a (store 4 'True a))

;; a

;; (setq a (store 5 'False a))

;; (setq a (store 6 'True a))

;; (setq a (store 3 10 a))

;; a

;; (lookup (operand 1 '(VARIABLE 'pos a 3)) a)
;; (exp '(VARIABLE 'pos b 3) a)

;; b + 2, where offset of b is 3:
;; (exp '(OP_PLUS 'p (VARIABLE 'p b 3) (INT_LITERAL 'p 2)) a)

;; b * 2:
;; (exp '(OP_MULT 'p (VARIABLE 'p b 3) (INT_LITERAL 'p 2)) a)

;; a*2+b, where offset of b is 1:
;; (exp '(OP_PLUS 'P (OP_MULT 'p (VARIABLE 'p a 3) (INT_LITERAL 'p 2))  (VARIABLE 'p b 1)) a)

;; a - 2:
;; (exp '(OP_MINUS 'p (VARIABLE 'p a 3) (INT_LITERAL 'p 2)) a)

;; a - b:
;; (exp '(OP_MINUS 'p (VARIABLE 'p a 3) (VARIABLE 'p b 1)) a)

;; (exp '(OP_DIV 'p (OP_MULT 'p (VARIABLE 'p a 0) (VARIABLE 'p b 3))  (OP_PLUS 'p (VARIABLE 'p a 0) (VARIABLE 'p b 3))) a)

;; (exp '(OP_DIV 'p (VARIABLE 'p a 0) (VARIABLE 'p b 3)) a)

;; (exp '(OP_OR 'p (VARIABLE 'p e 4)(VARIABLE 'p f 5) ) a)

;; (exp '(OP_AND 'p (VARIABLE 'p e 4)(VARIABLE 'p f 5) ) a)

;; (exp '(OP_NOT 'p (OP_OR 'p (VARIABLE 'p e 4)(VARIABLE 'p f 5) )) a)

;; (exp '(OP_OR 'p (OP_AND 'p (VARIABLE 'p e 4)(VARIABLE 'p f 5) ) (VARIABLE 'p g 6))  a)

;; (exp '(OP_EQ 'p (VARIABLE 'p a 9) (INT_LITERAL 'p 77)) (store 9 77 ()))

;; (exp '(OP_EQ 'p (VARIABLE 'p a 3) (INT_LITERAL 'p 10)) a)


(defun stmts (ast alist)
  "Interpret a statement or a sequence of statenents, return the store."
  ;; SEQ evaluates the right operand with the store returned by the left one.
  ;; DECL is simply skipped.
  ;; ASSIGNMENT evaluates the right operand and stores the result under the
  ;;            name of the second operand.
  ;; IF and WHILE are handled separately.
  ;; PRINT just evaluates and outputs its operand.
  (cond
   ((eq (kind ast) 'SEQ)          (stmts (operand 1 ast)
                                         (stmts (operand 0 ast) alist)
                                         ))
   ((eq (kind ast) 'DECL)         alist)
   ((eq (kind ast) 'ASSIGNMENT)   (store (operand 1 (operand 0 ast))
                                         (exp (operand 1 ast) alist)
                                         alist
                                         ))
   ((eq (kind ast) 'IF)           (if_stmt    ast alist))
   ((eq (kind ast) 'WHILE)        (while_stmt ast alist))
   ((eq (kind ast) 'PRINT_BOOL)   (progn
                                    (print (exp (operand 0 ast) alist))
                                    alist
                                    ))
   ((eq (kind ast) 'PRINT_INT)    (progn
                                    (print (exp (operand 0 ast) alist))
                                    alist
                                    ))
   )
  )

(defun if_stmt (ast alist)
  "Evaluate the AST for an IF node, returning the updated store."
  (if (eq 'True (exp (operand 0 ast) alist))      ; is condition true?
      (stmts (operand 1 ast) alist)               ; the "then" branch
    (stmts (operand 2 ast) alist)                 ; the "else" branch
    )
  )

(defun while_stmt (ast alist)
  "Evaluate the AST for a WHILE node, returning the updated store."
  (if (eq 'True (exp (operand 0 ast) alist))      ; is condition true?
      ;; yes: evaluate this ast again, in the store updated by the body
      (while_stmt ast (stmts (operand 1 ast) alist))
    ;; no: just return the store
    alist
    )
  )

(defun interpret (ast)
  "Interpret this AST."
  (stmts ast ())
  )


;; (interpret '(PRINT_INT pos (INT_LITERAL pos 17)) ())
;; (stmts '(PRINT_BOOL pos (BOOL_LITERAL pos True)) ())

(defun load_data (buffer-name)
  "Load the data from this buffer into variable `data`."
  (setq data (read (get-buffer buffer-name)))
  )

(defun run ()
  "Run the interpreter on data in `data`."
  (interpret data)
  )

;; Evaluate the following two expressions, after changing the buffer name to
;; the one you want.
;; NOTE: The buffer with data must be loaded first, and the cursor must be at
;;       the beginning.
;;
;; (load_data "if4.ast")
;; (run)

