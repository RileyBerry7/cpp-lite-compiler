//// PRIMARY DECLARATIONS
//template <typename T> ; // template_declaration
//extern template ;  // explicit_instantiation
//template <> ;              // explicit_specialization
//extern "C";                // linkage_specification
//[[myAttribute]];           // attribute_declaration <- declaration
//namespace newNamespace {;} // namespace_definition
//;                          // empty_declaration     <- declaration
//
//// SECONDARY DECLARATION
//asm("mov eax, 1"); // asm_definition
//namespace myNamespace = existingNamespace; // namespace_alias_definition
//using std::cout;                     // using declaration
//using namespace existingNamespace;   // using_directive
//static_assert (1, "Error Message."); // static_assert_declaration
//using myType = int; // alias_declaration       <- block_declaration
//enum colors;        // opaque_enum_declaration <- block_declaration

int * const * main()
{
    int *var1[];
    int ** A::B::C::* const * const volatile * &var1[10][20];
    char(var2); //static_cast
    (char)cast_var; // C style cast
    A::B::myType var3;
//  if (1 < 2 + 1 - 1 / 1){}
    return 0;

    foo + 1;
    foo;
    1 + 2 * 3 / 4 - 5 % 6;
    (int long*)42;
}
