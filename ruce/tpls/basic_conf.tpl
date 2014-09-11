env:
  use_env: '{{env_name}}'
  {{env_name}}: 'http://{{host}}:{{port}}'

http:
  get:
    timeout: 1
  post:
    timeout: 1

screen_print:
  http_url: 0
  http_code: 0
  http_body: 0

log_conf:
  - name: 'ruce'
    file: './log/ruce.log'
    level: 'INFO'
    format: '%(asctime)s %(levelname)s %(message)s %(filename)s:%(lineno)d'
