.PHONY: clean

README.md: report.Rmd report.R
	Rscript -e 'rmarkdown::render("$<", output_file = "$@", output_format = "github_document")'
clean:
	rm -rf README.md report_cache/ README_files/