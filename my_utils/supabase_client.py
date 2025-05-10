from supabase import create_client
import os

url = "https://mhwepdtjevqupglpurpn.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1od2VwZHRqZXZxdXBnbHB1cnBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY4ODU3NDEsImV4cCI6MjA2MjQ2MTc0MX0.fTvkTsfeCCYXR0GIPnkHz6tGbvBg6JBqlXBrSXmnpOM"

supabase = create_client(url, key)
