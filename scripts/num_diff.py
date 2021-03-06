import sys

if(len(sys.argv) != 3):
    print("NUM_DIFF_ERROR_INVALID_ARGS" , sys.argv);
    sys.exit(-1)

def is_numeric(x):
    try:
        val = float(x)
    except ValueError:
        return False;
    return True;
   
# the goal here is to compare the two words inside a JSON and
# allow some small numeric differences
# (used to compare dataframe.to_json() in the logs).

def compare_words(word_orig, word_new):
    if(word_orig == word_new):
        return 0;
    # print("DIFFERENT_WORDS" , word_orig, word_new)    
    if(is_numeric(word_orig) and is_numeric(word_new)):
        lNumber_orig = float(word_orig);
        lNumber_new = float(word_new);
        lDiff = abs(lNumber_new - lNumber_orig) / lNumber_orig;
        lDiff = abs(lDiff)
        if(lDiff > 1e-10):
            return 1;
        else:
            print("NUM_DIFF_DEBUG_ALLOWED_SMALL_DIFFERENCE", word_orig, word_new, lNumber_orig, lNumber_new, lDiff)
            return 0;
    else:
        # print("NUM_DIFF_NOT_NUMERIC_DIFF", word_orig, word_new)        
        return 1;
    

def compare_lines(line_orig, line_new):
    if(line_orig == line_new):
        return 0;
    # if both lines contain 'TIME' , skip.
    if('TIME' in line_orig.upper() and 'TIME' in line_new.upper()):
        return 0;
    import re
    lRegex  = '[?,:"{}] \n\t'
    split_orig = re.split(lRegex, line_orig)
    split_new = re.split(lRegex, line_new)
    # print(split_orig)
    # print(split_new)

    N_orig = len(split_orig)
    N_new = len(split_new)
    if(N_orig != N_new):
        print("NUM_DIFF_LINE_WITH_DIFFERENT_NUMBER_OF_WORDS" , N_orig, N_new);
        return 1;

    N = min(N_orig, N_new);
    # compare the first N words of the two lines.
    out = 0;
    for l in range(N):
        result = compare_words(split_orig[l] , split_new[l])
        out = out + result;
    
    return out;

def compare_files(file_orig, file_new):
    with open(file_orig) as f:
        content_orig = f.readlines()

    with open(file_new) as f:
        content_new = f.readlines()

    N_orig = len(content_orig)
    N_new = len(content_new)
    if(N_orig != N_new):
        print("NUM_DIFF_FILES_WITH_DIFFERENT_NUMBER_OF_LINES" , N_orig, N_new);

    lDiff = abs(N_orig - N_new)
    if(lDiff > 20):
       print("NUM_DIFF_FILES_WITH_TOO_MUCH_DIFF" , N_orig, N_new);
       print("NUM_DIFF_NUMBER_OF_DIFFERENT_LINES_AT_LEAST" , lDiff)
       print("NUM_DIFF_FILES_ARE_DIFFERENT")
       return;
        
    N = min(N_orig, N_new);
    # compare the first N lines of the two files.
    out = 0;
    diffs = [];
    for l in range(N):
        result = compare_lines(content_orig[l] , content_new[l])
        if(result > 0):
            diffs.append((content_orig[l] , content_new[l]));
        out = out + result;

    if(out > 0):
        print("NUM_DIFF_NUMBER_OF__DIFFERENT_LINES" , out)
        print(diffs[0])
        print(diffs[-1])
        print("#cp ", file_new, file_orig)
        print("NUM_DIFF_FILES_ARE_DIFFERENT")


file_orig = sys.argv[1]
file_new = sys.argv[2]

compare_files(file_orig, file_new);
