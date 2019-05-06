.PHONY: clean

report.md: report.Rmd report.R
	Rscript -e 'rmarkdown::render("$<", output_file = "$@")'
clean:
	rm -rf report.md report_cache/ report_files/