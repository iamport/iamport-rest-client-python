def test_find_user_pg(iamport):
    result = iamport.find_user_pg()
    assert result is not None
