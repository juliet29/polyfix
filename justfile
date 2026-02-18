update-deps:
  uv add /Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/utils4plans


trial-some:
  uv run snakemake -c 3 -k some --configfile "config/msd.yaml"
trial-all:
  uv run snakemake -c 3 -f -k all --configfile "config/msd.yaml"

trial-hard:
  uv run snakemake -c 3 -k some --configfile "config/msd_hard.yaml"

test-move path:
  echo "Processing file: {{path}}"
  uv run preproc trial-move "{{path}}"

# -------------- PUBLISH PACKAGE -------------
push-tag end:
  git tag -a s0.0.{{end}} -m s0.0.{{end}}
  git push --tag


publish-tag end:
  @echo "Have you updated the version number for pushing to pypi?" 
  @read status;


  @echo "Have you pushed the code with this new version number?" 
  @read status;

  git tag -a v0.0.{{end}} -m v0.0.{{end}}
  git push --tag
