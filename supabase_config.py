from supabase import create_client

SUPABASE_URL = "https://ahtmxrjptdrjtwbglieh.supabase.co"
SUPABASE_KEY = "sb_publishable_iPgRVakgsMnd8ogXb_QChQ_vYWdT2tX"

# create client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)