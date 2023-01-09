def sending_email():
    pass


"""    def send_email(self,
                   df: pd.DataFrame = None,
                   trading_type: str = None) -> None:
        
        Args:
            type_of_email: name from list ["trading info","error","confirmation"]
            df: optional attached dataframe
            paths_of_files_to_attach: list of files to send
        
        assert trading_type in ["fix1_vs_fix2"], \
            f"Error in trading_type argument - expected 'fix1_vs_fix2', got {trading_type}"

        type_of_email = "confirmation"
        paths_of_files_to_attach = None
        logger.info(f"Initializing sending {type_of_email} email")
        try:
            
                json settings:
                "email_from" : "axpotradingemailsender@gmail.com",
                "email_to" : ["piotr.srednicki@ds360.pl","axpotradingemailsender@gmail.com"],
                "password" : "pjgffxcwavsjbcjs"
            
            from_addr = self.ds360_credentials_json["email_from"]
            to_addrs = self.ds360_credentials_json["email_to"]
            password = self.ds360_credentials_json["password"]
        except Exception as e:
            logger.info(
                "The json file is misconfigured. Error message:", e)
            return

        title_of_email = f'{type_of_email} email generated on {datetime.date.today()}'
        if len(to_addrs) == 0:
            logger.info("There are no email receivers in the credentials")
            return

        try:
            for email in to_addrs:
                v = validate_email(email)
            logger.info("The mails are correct")
        except EmailNotValidError as e:
            logger.info("A receiving email is not valid. Error message: ", e)
            return

        try:
            msg = MIMEMultipart()
            msg.add_header('from', from_addr)
            msg.add_header('to', ' '.join([str(elem) + ',' for elem in to_addrs])[:-1])
            msg.add_header('subject', title_of_email)
            body_text = "Szanowni, wyniki backtestingu zostały wysłane do AXPO GCS bucket.\n\n"
            if trading_type == "fix1_vs_fix2":
                body_text += f'W mailu zamieszczone są propozycje propozycje tradingowe dla fix1_vs_fix2. dla dnia dzisiejszego: {datetime.date.today()}\n'
            body_text += f'Data rozpoczęcia procesu produkcji: {config_production_trading.production_trading_config["date_start"]}'
            msg.attach(MIMEText(str(body_text) + "\n\n", 'plain'))
            if df is not None:
                dataframe_to_text = str(df.to_markdown())
                msg.attach(MIMEText(dataframe_to_text + "\n\n", 'plain'))
            automatically_generated_text = f"Ta wiadomość została automatycznie wygenerowana przez DS360 AXPO TRADING.\n Proszę na Nią nie odpowiadać."
            msg.attach(MIMEText(str(automatically_generated_text), 'plain'))
        except Exception as e:
            logger.info(
                "Input data (one of from_addr,to_addrs,subject,content) is of wrong format. Error message: ", e)
            return

        try:
            attachment = MIMEApplication(df.to_csv(), Name = f'{datetime.date.today()}.csv')
            msg.attach(attachment)
        except Exception as e:
            logger.info("Adding csv file to the email failed. Error message: ", e)
            return

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        except Exception as e:
            logger.info("Wrong port. Change it to 465 or change server. Error message:", e)
            return

        try:
            server.connect('smtp.gmail.com', 465)
        except Exception as e:
            logger.info("Failed to connect to the server. Change port to 465 or change server. Error message:", e)
            return

        try:
            server.login(from_addr, password)
        except Exception as e:
            logger.info("Failed to log in to the server. Error message:", e)
            return

        try:
            server.send_message(msg, from_addr=from_addr, to_addrs=to_addrs)
        except Exception as e:
            logger.info("An error occured during sending the email. Error message:", e)
            return

        logger.info(f"The {type_of_email} email has been sent successfully")"""
