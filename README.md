# podcasts-api

## General

Project for uploading videos from YouTube as audio podcasts to TG and Soundcloud

[Detailed base architecture](Conversion%20Service.md)

## Subscribe for updates on a channel

Please follow instructions at [official YouTube data API page](https://developers.google.com/youtube/v3/guides/push_notifications). 
WebApp expects notifications on `/hooks/new/<channel_id>` endpoint.
