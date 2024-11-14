while getopts ":i:o:f:" opt; do
  case ${opt} in
    i )
      INPUT_FILE=$OPTARG
	  echo "== $INPUT_FILE =="
      ;;
	f )
	  INPUT_FOLDER=$OPTARG
	  echo "== $INPUT_FOLDER =="
	  ;;
	o )
	  OUTPUT_DIR=$OPTARG
	  echo "== $OUTPUT_DIR =="
	  ;;
    \? )
      echo "Invalid option: -$OPTARG" >&2
	  exit 1
      ;;
  esac
done

# Fix path to Logo
sed -i 's/template/ops-document-template/g' ops-document-template/template.sty

# Check if both arguments are provided
if [ -z "$INPUT_FILE" && -z "$INPUT_FOLDER"]; then
  echo "Error: Input file is required. -i or -f" >&2
  exit 1
fi

if [ -z "$OUTPUT_DIR" ]; then
  echo "Error: Output directory is required. -o" >&2
  exit 1
fi

# Commands for one file
if [ -n "$INPUT_FILE" ]; then
	FILENAME=$(basename $INPUT_FILE)
	python markdown_tex_generator.py -i $INPUT_FILE -o $OUTPUT_DIR
	lualatex -synctex=1  --output-directory=${OUTPUT_DIR} $OUTPUT_DIR/${FILENAME%.md}.tex
	lualatex -synctex=1  --output-directory=${OUTPUT_DIR} $OUTPUT_DIR/${FILENAME%.md}.tex
fi

if [ -n "$INPUT_FOLDER" ]; then
	for FILE in $INPUT_FOLDER/*.md; do
		FILENAME=$(basename $FILE)
		python markdown_tex_generator.py -i $FILE -o $OUTPUT_DIR
		lualatex -synctex=1  --output-directory=${OUTPUT_DIR} $OUTPUT_DIR/${FILENAME%.md}.tex
		lualatex -synctex=1  --output-directory=${OUTPUT_DIR} $OUTPUT_DIR/${FILENAME%.md}.tex
	done
fi

# Clean up
cd $OUTPUT_DIR
rm *.aux *.log *.out *.synctex.gz

