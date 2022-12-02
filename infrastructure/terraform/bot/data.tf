data "http" "github_tag" {
  url = "https://api.github.com/repos/alexraskin/lhbot/tags"

  request_headers = {
    Accept = "application/json"
  }
}
