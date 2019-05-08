.PHONY: clean

report.md: report.Rmd report.R
	Rscript -e 'rmarkdown::render("$<", output_file = "$@", output_format = "github_document")'
clean:
	rm -rf report.md report_cache/ report_files/