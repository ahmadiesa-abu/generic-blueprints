data "aws_iam_policy_document" "s3-bucket-policy" {

  statement {
    actions   = ["s3:ListBucket"]
    effect    = "Allow"
    resources = ["arn:aws:s3:::${var.bucket_name}"]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
  statement {
    actions   = ["s3:PutObject", "s3:GetObject", "s3:GetObjectVersion", "s3:DeleteObject", "s3:PutObjectAcl"]
    effect    = "Allow"
    resources = ["arn:aws:s3:::${var.bucket_name}/*"]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}
