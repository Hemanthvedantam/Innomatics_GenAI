import streamlit as st
import re
import difflib
import traceback

# Enhanced error patterns with individual regex flags
ERROR_PATTERNS = [
    {   # Incorrect numpy import
        'pattern': r'^import\s+numpy\s+as\s+NP\b',
        'flags': re.IGNORECASE,
        'fix': 'import numpy as np',
        'error': 'Incorrect numpy import capitalization',
        'category': 'Numpy'
    },
    {   # Uppercase numpy functions
        'pattern': r'np\.(Rand|Zeros|Ones|Empty|Arange)\(',
        'flags': 0,
        'fix': lambda m: f'np.{m.group(1).lower()}(',
        'error': 'Numpy function should be lowercase',
        'category': 'Numpy'
    },
    {   # Extra space in print
        'pattern': r'print\s\(',
        'flags': 0,
        'fix': 'print(',
        'error': 'Extra space after print statement',
        'category': 'Syntax'
    },
    {   # Range spacing
        'pattern': r'range\(\s*(\d+)\s*,\s*(\d+)\s*\)',
        'flags': 0,
        'fix': lambda m: f'range({m.group(1)}, {m.group(2)})',
        'error': 'Improper spacing in range function',
        'category': 'Syntax'
    },
    {   # == None comparison
        'pattern': r'==\s*None\b',
        'flags': 0,
        'fix': 'is None',
        'error': 'Use "is None" for None comparison',
        'category': 'Comparison'
    },
    {   # != None comparison
        'pattern': r'!=\s*None\b',
        'flags': 0,
        'fix': 'is not None',
        'error': 'Use "is not None" instead of "!= None"',
        'category': 'Comparison'
    },
    {   # Bare except clause
        'pattern': r'except\s*:',
        'flags': 0,
        'fix': 'except Exception:',
        'error': 'Bare except clause, specify the exception type',
        'category': 'Error Handling'
    },
    {   # Type comparison
        'pattern': r'type\((\w+)\)\s*==\s*(\w+)',
        'flags': 0,
        'fix': lambda m: f'isinstance({m.group(1)}, {m.group(2)})',
        'error': 'Use isinstance() instead of comparing types directly',
        'category': 'Type Check'
    },
    {   # 'is' with literals
        'pattern': r'\b(is|is not)\s+(\d+|[\'"][^\'"]+[\'"])',
        'flags': 0,
        'fix': lambda m: f'{"==" if m.group(1) == "is" else "!="} {m.group(2)}',
        'error': 'Using "is" with literal, use "==" instead',
        'category': 'Comparison'
    }
]

# Precompile regex patterns
COMPILED_PATTERNS = []
for p in ERROR_PATTERNS:
    try:
        regex = re.compile(p['pattern'], flags=p.get('flags', 0))
        COMPILED_PATTERNS.append({
            'regex': regex,
            'fix': p['fix'],
            'error': p['error'],
            'category': p['category']
        })
    except re.error as e:
        st.error(f"Error compiling pattern {p['pattern']}: {str(e)}")

def analyze_code(code, selected_categories):
    errors = []
    corrected_lines = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines):
        line_errors = []
        corrected_line = line
        
        for cp in COMPILED_PATTERNS:
            if cp['category'] not in selected_categories:
                continue
            regex = cp['regex']
            fix = cp['fix']
            error_msg = cp['error']
            
            if regex.search(line):
                line_errors.append(error_msg)
                try:
                    if callable(fix):
                        corrected_line = regex.sub(fix, corrected_line)
                    else:
                        corrected_line = regex.sub(fix, corrected_line)
                except Exception as e:
                    st.error(f"Error applying fix: {str(e)}")
        
        if line_errors:
            errors.append(f"Line {i+1}: {'; '.join(line_errors)}")
        corrected_lines.append(corrected_line)
    
    return errors, '\n'.join(corrected_lines)

def show_diff(original, corrected):
    diff = difflib.unified_diff(
        original.split('\n'),
        corrected.split('\n'),
        fromfile='Original',
        tofile='Corrected',
        lineterm=''
    )
    return '\n'.join(diff)

def main():
    st.title("🔍 Advanced Rule-Based Code Reviewer")
    st.markdown("Detect and fix common Python errors with enhanced checks")
    
    # Category selection
    categories = sorted(list({cp['category'] for cp in COMPILED_PATTERNS}))
    selected_categories = st.sidebar.multiselect(
        "Select checks to perform:",
        categories,
        default=categories
    )
    
    # Sample code loader
    if st.sidebar.button("Load Sample Code"):
        sample_code = """import NUMPY as NP

arr = NP.Rand(3)
print (arr)
x = 5
if x is 5:
    print("x is 5")
if y == None:
    pass
try:
    pass
except:
    pass
"""
        st.session_state.sample_code = sample_code
    
    code = st.text_area("Input Python code:", height=300,
                        value=st.session_state.get('sample_code', 
                        "import NUMPY as NP\n\narr = NP.Rand(3)\nprint (arr)"))
    
    if st.button("Analyze Code"):
        errors, fixed_code = analyze_code(code, selected_categories)
        
        with st.expander("Original Code"):
            st.code(code, language='python')
        
        if errors:
            st.subheader("🔧 Found Issues")
            for error in errors:
                st.error(error)
            
            st.subheader("🔀 Diff View")
            diff_output = show_diff(code, fixed_code)
            st.text(diff_output)
            
            st.subheader("✅ Corrected Code")
            st.code(fixed_code, language='python')
            
            if st.button("Test Fixed Code"):
                try:
                    exec(fixed_code)
                    st.success("Code executed successfully!")
                except Exception as e:
                    st.error(f"Execution error: {str(e)}")
                    tb = traceback.extract_tb(e.__traceback__)
                    for frame in tb:
                        if frame.filename == '<string>':
                            st.error(f"Error at line {frame.lineno}: {frame.line}")
        else:
            st.success("🎉 No issues found!")

    st.sidebar.markdown("### Enhanced Checks")
    st.sidebar.write("- Numpy imports/functions\n"
                     "- Print/range syntax\n- None comparisons\n- Bare except clauses\n"
                     "- Type checking\n- Literal comparisons")

if __name__ == "__main__":
    main()