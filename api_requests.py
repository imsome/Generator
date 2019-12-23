# coding=utf-8

register = "v3/user/register"
authorize = "v3/user/login"
watch_ad = "v3/ad/view/"
create_ad_old = "v3/ad/create"
upload_image = "v3/image/upload"
update_user = "v3/user/update"
set_new_language = "v3/user/set-language"
advert_create = "v3/advert/create"

#
# DB QUERIES
#
query_set_status_confirmed = "UPDATE ads SET status = 2 WHERE status != 2"
query_get_ads_min_and_max = "SELECT min(id), max(id) FROM ads"
