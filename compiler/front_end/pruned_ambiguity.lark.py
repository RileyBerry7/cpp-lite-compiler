# The following rules were replaced or pruned(deleted) to resolve ambiguities in the grammar:

# Replaced with 'ambiguous_identifier'.

# A.1
ambiguous_identifier: IDENTIFIER


# A.2

# A.4
unqualified_id: IDENTIFIER
              | operator_function_id
              | conversion_function_id
              | literal_operator_id
              | BIT_NOT decltype_specifier
              | template_id
              | BIT_NOT ambiguous_identifier   # <- Pruned class_name
              | BIT_NOT simple_template_id     # <- Lifted from class_name
#ISO:         | BIT_NOT class_name

# A.6
##########################
#  NAMESPACE DEFINITION  #
##########################
namespace_definition: named_namespace_definition
                    | unnamed_namespace_definition

#ISO: named_namespace_definition: original_namespace_definition  <- Collapsed ambiguity
#                               | extension_namespace_definition <- Collapsed ambiguity
named_namespace_definition: INLINE? NAMESPACE namespace_name _LBRACE namespace_body _RBRACE
# |--> Lifted from extension 'ext_namespace_def' & 'original_namespace_def"

#ISO: extension_namespace_definition: INLINE? NAMESPACE original_namespace_name _LBRACE namespace_body _RBRACE

#ISO: original_namespace_definition: INLINE? NAMESPACE IDENTIFIER _LBRACE namespace_body _RBRACE

# A.6.1
#ISO: namespace_name: ambiguous_identifier <- Pruned into ambiguous_identifier
#                   | namespace_alias
namespace_name: ambiguous_identifier # <- Re-aliased into ambiguous_identifier

#ISO: original_namespace_name: IDENTIFIER <- Pruned into ambiguous_identifier

#ISO: namespace_alias: IDENTIFIER <- Pruned into ambiguous_identifier

# A.6.2
#ISO: enum_name: IDENTIFIER <- Pruned into ambiguous_identifier

# A.6.3
#ISO: typedef_name: IDENTIFIER <- Pruned into ambiguous_identifier

#ISO: type_name: class_name
#          | enum_name
#          | typedef_name
type_name: ambiguous_identifier # <- Collapsed ambiguity
         | simple_template_id   # <- Lifted from class_name

# A.7
declarator_id: ELLIPSIS? id_expression
             | SCOPE? nested_name_specifier? ambiguous_identifier   # <- Pruned class_name
             | SCOPE? nested_name_specifier? simple_template_id     # <- Lifted from class_name
#ISO:        | SCOPE? nested_name_specifier? class_name             # -> Collapsed ambiguity

# A.8

#ISO: class_name: IDENTIFIER          <- Pruned into ambiguous_identifier
#               | simple_template_id  <- Factor out non-ambiguity

# A.9
class_or_decltype: decltype_specifier
                 | SCOPE? nested_name_specifier? ambiguous_identifier   # <- Pruned class_name
                 | SCOPE? nested_name_specifier? simple_template_id     # <- Lifted from class_name
#ISO:            | SCOPE? nested_name_specifier? class_name             # -> Collapsed ambiguity