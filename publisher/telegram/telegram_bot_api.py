import urllib

import requests


class TelegramBot:
    """
    The Bot API is an HTTP-based interface created for developers keen on building bots for Telegram.
    docs: https://core.telegram.org/bots/api#recent-changes
    """

    def __init__(self, token, server=None):
        if server is None or server[:4] != 'http':
            server = 'https://api.telegram.org'
        self.__server = server
        self.__token = token

    def request(self, method_name, json=None, files=None, args=None):
        """Send request to telegram api server
        :return None if request finished with error or telegram does not return 'result' in response json
        :return 'result' section from response json if ok
        """
        if files is not None:
            if json is not None and args is not None:
                args = {**json, **args}
            elif args is None:
                args = json
            json = dict()
        if json is None:
            json = dict()
        args = '&'.join([f'{k}={urllib.parse.quote_plus(str(v))}' for k, v in self.__filter(**args).items()]) if args is not None else ''
        response = requests.post(f'{self.__server}/bot{self.__token}/{method_name}?{args}',
                                 json=self.__filter(**json),
                                 files=files)
        if response.status_code == 200 and (json := response.json()) and \
                'ok' in json and json['ok'] is True and 'result' in json:
            return json['result']
        else:
            return None

    def __filter(self, **kwargs):
        """
        Filter arguments with not None value
        :return dict
        """
        return dict([(k, v) for k, v in kwargs.items() if v is not None])

    def set_webhook(self, url, certificate=None, ip_address=None, max_connections=None, allowed_updates=None,
                    drop_pending_updates=None):
        """Use this method to specify a url and receive incoming updates via an outgoing webhook. Whenever there is an
        update for the bot, we will send an HTTPS POST request to the specified url, containing a JSON-serialized
        Update. In case of an unsuccessful request, we will give up after a reasonable amount of attempts. Returns
        True on success.
        If you'd like to make sure that the Webhook request comes from Telegram, we recommend using a secret path in
        the URL, e.g. https://www.example.com/<token>. Since nobody else knows your bot's token, you can be pretty
        sure it's us.
        Parameter               Type	        Required	Description
        url                     String	        Yes	        HTTPS url to send updates to. Use an empty string to remove webhook integration
        certificate             InputFile	    Optional	Upload your public key certificate so that the root certificate in use can be checked. See our self-signed guide for details.
        ip_address              String	        Optional	The fixed IP address which will be used to send webhook requests instead of the IP address resolved through DNS
        max_connections         Integer	        Optional	Maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
        allowed_updates         Array of String Optional	A JSON-serialized list of the update types you want your bot to receive. For example, specify [“message”, “edited_channel_post”, “callback_query”] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member (default). If not specified, the previous setting will be used.
                                                            Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time.
        drop_pending_updates    Boolean	        Optional	Pass True to drop all pending updates
        """
        return self.request('setWebhook', json=self.__filter(
            url=url,
            certificate=certificate,
            ip_address=ip_address,
            max_connections=max_connections,
            allowed_updates=allowed_updates,
            drop_pending_updates=drop_pending_updates,
        ))

    def delete_webhook(self, drop_pending_updates=None):
        """Use this method to remove webhook integration if you decide to switch back to getUpdates. Returns True on success.
        Parameter	            Type	Required	Description
        drop_pending_updates	Boolean	Optional	Pass True to drop all pending updates
        """
        return self.request('deleteWebhook', json=self.__filter(
            drop_pending_updates=drop_pending_updates
        ))

    def get_me(self):
        """A simple method for testing your bot's authentication token. Requires no parameters.
        Returns basic information about the bot in form of a User object."""
        return self.request('getMe')

    def send_message(self, chat_id, text, parse_mode=None, entities=None, disable_web_page_preview=None,
                     disable_notification=None, protect_content=None, reply_to_message_id=None,
                     allow_sending_without_reply=None, reply_markup=None):
        """Use this method to send text messages. On success, the sent Message is returned.
        Parameter                   Type	                Required    Description
        chat_id	                    Integer or String       Yes         Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        text	                    String                  Yes         Text of the message to be sent, 1-4096 characters after entities parsing
        parse_mode                  String                  Optional	Mode for parsing entities in the message text. See formatting options for more details.
        entities                    Array of MessageEntity  Optional	A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
        disable_web_page_preview	Boolean	                Optional	Disables link previews for links in this message
        disable_notification	    Boolean	                Optional	Sends the message silently. Users will receive a notification with no sound.
        protect_content	            Boolean	                Optional	Protects the contents of the sent message from forwarding and saving
        reply_to_message_id	        Integer	                Optional	If the message is a reply, ID of the original message
        allow_sending_without_reply	Boolean	                Optional	Pass True, if the message should be sent even if the specified replied-to message is not found
        reply_markup                InlineKeyboardMarkup or Optional	Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
                                    ReplyKeyboardMarkup or
                                    ReplyKeyboardRemove or
                                    ForceReply
        """
        return self.request('sendMessage', json=self.__filter(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        ))

    def send_photo(self, chat_id, photo, caption=None, parse_mode=None, caption_entities=None, disable_notification=None,
                   protect_content=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """Use this method to send photos. On success, the sent Message is returned.
        Online docs: https://core.telegram.org/bots/api#sendphoto
        Parameter	                Type	                Required	Description
        chat_id	                    Integer or String	    Yes	        Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        photo	                    InputFile or String	    Yes	        Photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a photo from the Internet, or upload a new photo using multipart/form-data. The photo must be at most 10 MB in size. The photo's width and height must not exceed 10000 in total. Width and height ratio must be at most 20. More info on Sending Files »
        caption	                    String	                Optional	Photo caption (may also be used when resending photos by file_id), 0-1024 characters after entities parsing
        parse_mode	                String	                Optional	Mode for parsing entities in the photo caption. See formatting options for more details.
        caption_entities	        Array of MessageEntity	Optional	A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        disable_notification	    Boolean	                Optional	Sends the message silently. Users will receive a notification with no sound.
        protect_content	            Boolean	                Optional	Protects the contents of the sent message from forwarding and saving
        reply_to_message_id	        Integer	                Optional	If the message is a reply, ID of the original message
        allow_sending_without_reply Boolean	                Optional	Pass True, if the message should be sent even if the specified replied-to message is not found
        reply_markup	            InlineKeyboardMarkup or Optional	Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
                                    ReplyKeyboardMarkup or
                                    ReplyKeyboardRemove or
                                    ForceReply
        """
        data = dict(
            chat_id=chat_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        json = files = args = None
        if isinstance(photo, str):
            json = data
            json['photo'] = photo
        else:
            args = data
            files = dict(photo=photo)
        return self.request('sendPhoto', json, files, args)

    def send_audio(self, chat_id, audio, caption=None, parse_mode=None, caption_entities=None, duration=None,
                   performer=None, title=None, thumb=None, disable_notification=None, protect_content=None,
                   reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """Use this method to send audio files, if you want Telegram clients to display them in the music player. Your
        audio must be in the .MP3 or .M4A format. On success, the sent Message is returned. Bots can currently send
        audio files of up to 50 MB in size, this limit may be changed in the future.
        For sending voice messages, use the sendVoice method instead.
        Online docs: https://core.telegram.org/bots/api#sendaudio
        Parameter	                Type	                Required	Description
        chat_id	                    Integer or String	    Yes	        Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        audio	                    InputFile or String	    Yes	        Audio file to send. Pass a file_id as String to send an audio file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an audio file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files »
        caption	                    String	                Optional	Audio caption, 0-1024 characters after entities parsing
        parse_mode	                String	                Optional	Mode for parsing entities in the audio caption. See formatting options for more details.
        caption_entities	        Array of MessageEntity	Optional	A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        duration	                Integer	                Optional	Duration of the audio in seconds
        performer	                String	                Optional	Performer
        title	                    String	                Optional	Track name
        thumb	                    InputFile or String	    Optional	Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files »
        disable_notification	    Boolean	                Optional	Sends the message silently. Users will receive a notification with no sound.
        protect_content	            Boolean	                Optional	Protects the contents of the sent message from forwarding and saving
        reply_to_message_id         Integer	                Optional	If the message is a reply, ID of the original message
        allow_sending_without_reply Boolean	                Optional	Pass True, if the message should be sent even if the specified replied-to message is not found
        reply_markup	            InlineKeyboardMarkup or Optional	Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
                                    ReplyKeyboardMarkup or
                                    ReplyKeyboardRemove or
                                    ForceReply
        """
        data = dict(
            chat_id=chat_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        json = files = args = None
        if isinstance(audio, str) and (isinstance(thumb, str) or thumb is None):
            json = data
            json['audio'] = audio
            json['thumb'] = thumb
        elif not isinstance(audio, str) and not isinstance(thumb, str):
            args = data
            files = dict(
                audio=audio,
                thumb=thumb
            )
        elif not isinstance(audio, str):
            args = data
            args['thumb'] = thumb
            files = dict(audio=audio)
        else:
            args = data
            args['audio'] = audio
            files = dict(thumb=thumb)
        return self.request('sendAudio', json, files, args)
