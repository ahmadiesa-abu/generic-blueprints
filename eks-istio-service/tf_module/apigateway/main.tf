// API Gateway stuff
resource "aws_apigatewayv2_api" "apigway" {
  name          =  var.api_gw_name
  protocol_type = "HTTP"
  description   = "API Gwy HTTP API and URL Endpoint"
}


resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.apigway.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "app" {
  api_id = aws_apigatewayv2_api.apigway.id
  integration_uri    = var.url_endpoint
  integration_type   = "HTTP_PROXY"
  integration_method = "ANY"
}

resource "aws_apigatewayv2_route" "any" {
  api_id = aws_apigatewayv2_api.apigway.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.app.id}"
}
