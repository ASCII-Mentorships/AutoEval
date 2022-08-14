import sys
import os
import json

def construct_input():
    fp = open('template.json')
    data = json.load(fp)
    input =  "int main()\n{\n\t"
    # Get function detail
    # Get details of arguments
    scalar_arguments = data['inputParams']
    array_arguments = data['arrayConfig']

    # Declare the input variables
    golden_arguments = ""
    student_arguments = ""
    golden_function_name = data['goldenSolution']['fname']
    student_function_name = data['studentSolution']['fname']
    student_argValType = ""
    golden_argValType = ""

    for x in scalar_arguments:
        type = x['type']
        name = x['name']
        input = input + type + " " + name + ";\n\tklee_make_symbolic(&" + name + ",sizeof(" + name + "),\"" + name + "\");\n\n\t"
        golden_arguments = golden_arguments + "," + name
        student_arguments = student_arguments + "," + name
        student_argValType = student_argValType + ", "+type +" "+name
        golden_argValType = golden_argValType + ", "+type +" "+name

    for x in array_arguments:
        type = x['type']
        name = x['name']
        value = x['size']
        if value is not None:
            input = input + "int" + " " + name + "_size = " + value + ";\n\t"
            input = input + type + " " + name + "[" + name + "_size" + "];\n\tklee_make_symbolic(&" + name + ",sizeof(" + name + "),\"" + name + "\");\n\t"
            input = input + type + " " + name + "_copy[" + name + "_size" + "];\n\tmemcpy(" + name + "_copy" +"," + name +",sizeof(" + name +"));\n\n\t"
            golden_arguments = golden_arguments + "," + name + "," + name + "_size"
            student_arguments = student_arguments + "," + name + "_copy" + "," + name + "_size"
            student_argValType = student_argValType + ", "+type +" "+ name + "_copy" + "," +"int "+ name + "_size"
            golden_argValType = golden_argValType + ", "+type +" "+ name + "_copy" + "," +"int "+ name + "_size"
        elif value is None and name is not None:
            sys.stderr.write("Non static array sizes not supported for KLEE\n")
            exit()

    golden_arguments = golden_arguments[1:]    
    student_arguments = student_arguments[1:]
    student_argValType = student_argValType[1:]
    golden_argValType = golden_argValType[1:]

    input = input + data['outputParam']['type'] + " return_value_1 = " + golden_function_name + "(" + golden_arguments + ");\n\t"
    input = input + data['outputParam']['type'] + " return_value_2 = " + student_function_name + "(" + student_arguments + ");\n\n\t"

    input = input + "if(precondition(" + golden_arguments + ") == 1 && semantic_category(" + golden_arguments + ")  == 1)\n\t{\n\t\t"
    input = input + "assert(postcondition(" + golden_arguments + ",return_value_1,return_value_2) == 1);\n\t}\n\treturn 0;\n}"

    input = data['postCondition'] + "\n\n" + input
    input = data['preCondition']+"\n\n" + input 
    input = data['goldenSolution']['solution']+"\n\n" + input 
    input = data['outputParam']['type'] +" "+data['studentSolution']['fname']+"(" + student_argValType+ ");\n\n" + input 
    input  =  "int semantic_category(" + golden_argValType+ ");\n\n" + input 
    input = "#include<stdio.h>\n#include<stdlib.h>\n#include<assert.h>\n#include<string.h>\n\n" + input

    fp.close()
    print(input)
    return input


construct_input()



