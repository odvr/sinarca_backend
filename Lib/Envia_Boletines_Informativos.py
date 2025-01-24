import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.db import remitente,password,servidor_smtp,puerto_smtp
def enviar_Boletines(destinatario, asunto,Notificacion):
    """
    Envía un correo electrónico de tipo notificación a un usuario.

    Esta función permite realizar el envío de correos electrónicos con un formato de notificación.
    Es ideal para notificar a los usuarios sobre eventos, alertas o cualquier tipo de comunicación.

    Parámetros:
    :param destinatario: str
        Dirección de correo electrónico del destinatario.
    :param asunto: str
        Asunto del correo que aparecerá en la bandeja de entrada del destinatario.
    :param notificacion: str
        Contenido o cuerpo del correo electrónico. Este será el mensaje que se enviará al cliente.

    Retorno:
    :return: None
        La función no devuelve ningún valor. Su propósito es realizar el envío del correo.

    Ejemplo de uso:
    enviar_correo("usuario@example.com", "Recordatorio", "Estimado usuario, le recordamos que...")

    Notas:
    - Asegúrese de que el servidor de correo esté configurado correctamente antes de utilizar esta función.
    - Maneje posibles excepciones para garantizar que errores en el envío no interrumpan el flujo principal de la aplicación.
    """

    mensaje = """
    
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="es">
 <head>
  <meta charset="UTF-8">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <meta name="x-apple-disable-message-reformatting">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta content="telephone=no" name="format-detection">
  <title>Nueva plantilla de correo electrónico 2025-01-22</title><!--[if (mso 16)]><style type="text/css"> a {text-decoration: none;} </style><![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if !mso]><!-- -->
  <link href="https://fonts.googleapis.com/css?family=Montserrat:500,800" rel="stylesheet"><!--<![endif]--><!--[if gte mso 9]>
<noscript>
         <xml>
           <o:OfficeDocumentSettings>
           <o:AllowPNG></o:AllowPNG>
           <o:PixelsPerInch>96</o:PixelsPerInch>
           </o:OfficeDocumentSettings>
         </xml>
      </noscript>
<![endif]--><!--[if mso]><xml>
    <w:WordDocument xmlns:w="urn:schemas-microsoft-com:office:word">
      <w:DontUseAdvancedTypographyReadingMail/>
    </w:WordDocument>
    </xml><![endif]-->
  <style type="text/css">.rollover:hover .rollover-first {
	max-height:0px!important;
	display:none!important;
}
.rollover:hover .rollover-second {
	max-height:none!important;
	display:block!important;
}
.rollover span {
	font-size:0px;
}
u + .body img ~ div div {
	display:none;
}
#outlook a {
	padding:0;
}
span.MsoHyperlink,
span.MsoHyperlinkFollowed {
	color:inherit;
	mso-style-priority:99;
}
a.n {
	mso-style-priority:100!important;
	text-decoration:none!important;
}
a[x-apple-data-detectors],
#MessageViewBody a {
	color:inherit!important;
	text-decoration:none!important;
	font-size:inherit!important;
	font-family:inherit!important;
	font-weight:inherit!important;
	line-height:inherit!important;
}
.d {
	display:none;
	float:left;
	overflow:hidden;
	width:0;
	max-height:0;
	line-height:0;
	mso-hide:all;
}
a.n:hover {
	border-color:#2CB543!important;
	background:#2CB543!important;
}
a.es-secondary:hover {
	border-color:#ffffff!important;
	background:#ffffff!important;
}
@media only screen and (max-width:600px) {h1 { font-size:30px!important; text-align:center } h2 { font-size:26px!important; text-align:center } h3 { font-size:20px!important; text-align:center } .bd { padding-right:0px!important } .bc { padding-bottom:20px!important }  *[class="gmail-fix"] { display:none!important } p, a { line-height:150%!important } h1, h1 a { line-height:120%!important } h2, h2 a { line-height:120%!important } h3, h3 a { line-height:120%!important } h4, h4 a { line-height:120%!important } h5, h5 a { line-height:120%!important } h6, h6 a { line-height:120%!important }  .z p { }  .x p { } h4 { font-size:24px!important; text-align:left } h5 { font-size:20px!important; text-align:left } h6 { font-size:16px!important; text-align:left }        .ba p, .ba a { font-size:16px!important } .z p, .z a { font-size:16px!important }  .x p, .x a { font-size:12px!important } .u, .u h1, .u h2, .u h3, .u h4, .u h5, .u h6 { text-align:center!important }   .v, .v h1, .v h2, .v h3, .v h4, .v h5, .v h6 { text-align:left!important } .t img, .u img, .v img { display:inline!important } .t .rollover:hover .rollover-second, .u .rollover:hover .rollover-second, .v .rollover:hover .rollover-second { display:inline!important }   a.n, button.n { font-size:16px!important; padding:10px 20px 10px 20px!important; line-height:120%!important } a.n, button.n, .r { display:block!important }  .m, .m .n, .o, .o td, .b { display:inline-block!important }  .g table, .h table, .i table, .g, .i, .h { width:100%!important; max-width:600px!important } .adapt-img { width:100%!important; height:auto!important }       table.a, .esd-block-html table { width:auto!important } .h-auto { height:auto!important } u + #body { width:100vw!important } }
@media screen and (max-width:384px) {.mail-message-content { width:414px!important } }</style>
 </head>
 <body class="body" style="width:100%;height:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
  <div dir="ltr" class="es-wrapper-color" lang="es" style="background-color:#F7F7F7"><!--[if gte mso 9]>
			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
				<v:fill type="tile" color="#F7F7F7"></v:fill>
			</v:background>
		<![endif]-->
   <table cellpadding="0" cellspacing="0" width="100%" class="es-wrapper" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#F7F7F7">
     <tr style="border-collapse:collapse">
      <td valign="top" style="padding:0;Margin:0">
       <table cellpadding="0" cellspacing="0" align="center" class="h" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important;background-color:#34265F;background-repeat:repeat;background-position:center bottom">
         <tr style="border-collapse:collapse">
          <td align="center" bgcolor="#93c47d" background="https://ffzppoq.stripocdn.email/content/guids/CABINET_3a7a698c62586f3eb3e12df4199718b8/images/6941564382201394.png" style="padding:0;Margin:0;background-image:url(https://ffzppoq.stripocdn.email/content/guids/CABINET_3a7a698c62586f3eb3e12df4199718b8/images/6941564382201394.png);background-color:#93c47d;background-position:center bottom;background-repeat:repeat">
           <table cellspacing="0" cellpadding="0" align="center" bgcolor="transparent" class="ba" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr style="border-collapse:collapse">
              <td align="left" style="Margin:0;padding-top:20px;padding-right:20px;padding-bottom:25px;padding-left:20px;background-position:center bottom">
               <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr style="border-collapse:collapse">
                  <td valign="top" align="center" style="padding:0;Margin:0;width:560px">
                   <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:center bottom">
                     <tr style="border-collapse:collapse">
                      <td align="center" class="u" style="padding:0;Margin:0;font-size:0"><a href="https://sinarca.co/" target="_blank" style="mso-line-height-rule:exactly;text-decoration:underline;color:#FFFFFF;font-size:14px"><img src="https://ffzppoq.stripocdn.email/content/guids/c5d034cf-65cb-4438-ad5d-9eeaffc4b4fe/images/logoct_1_removebgpreview_1_1.png" alt="Ruta Ganadera" title="Ruta Ganadera" width="99" style="display:block;font-size:16px;border:0;outline:none;text-decoration:none"></a></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" align="center" class="g" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important">
         <tr style="border-collapse:collapse">
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" class="z" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr style="border-collapse:collapse">
              <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-right:30px;padding-left:30px;background-position:center bottom">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr style="border-collapse:collapse">
                  <td align="center" valign="top" style="padding:0;Margin:0;width:540px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr style="border-collapse:collapse">
                      <td align="left" style="padding:0;Margin:0;padding-bottom:5px"><h1 style="Margin:0;font-family:Montserrat, Helvetica, Roboto, Arial, sans-serif;mso-line-height-rule:exactly;letter-spacing:0;font-size:32px;font-style:normal;font-weight:bold;line-height:38.4px;color:#4A4A4A">📢 Boletín Informativo</h1></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" align="center" class="g" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important">
         <tr style="border-collapse:collapse">
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" class="z" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr style="border-collapse:collapse">
              <td align="left" bgcolor="#ffffff" style="Margin:0;padding-top:20px;padding-right:20px;padding-bottom:20px;padding-left:10px;background-position:left top;background-color:#ffffff;border-radius:13px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr style="border-collapse:collapse">
                  <td align="left" style="padding:0;Margin:0;width:570px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr style="border-collapse:collapse">
                      <td align="left" style="padding:0;Margin:0;padding-bottom:5px;padding-top:5px"><p style="Margin:0;mso-line-height-rule:exactly;font-family:Montserrat, Helvetica, Roboto, Arial, sans-serif;line-height:24px;letter-spacing:0;color:#4A4A4A;font-size:16px"><br></p><p style="Margin:0;mso-line-height-rule:exactly;font-family:Montserrat, Helvetica, Roboto, Arial, sans-serif;line-height:24px;letter-spacing:0;color:#4A4A4A;font-size:16px">{{NotificacionesCorreo}}</p><p style="Margin:0;mso-line-height-rule:exactly;font-family:Montserrat, Helvetica, Roboto, Arial, sans-serif;line-height:24px;letter-spacing:0;color:#4A4A4A;font-size:16px"><br></p><p style="Margin:0;mso-line-height-rule:exactly;font-family:Montserrat, Helvetica, Roboto, Arial, sans-serif;line-height:24px;letter-spacing:0;color:#4A4A4A;font-size:16px"><br></p><p style="Margin:0;mso-line-height-rule:exactly;font-family:Montserrat, Helvetica, Roboto, Arial, sans-serif;line-height:24px;letter-spacing:0;color:#4A4A4A;font-size:16px"><br></p><p style="Margin:0;mso-line-height-rule:exactly;font-family:Montserrat, Helvetica, Roboto, Arial, sans-serif;line-height:24px;letter-spacing:0;color:#4A4A4A;font-size:16px"><br></p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" align="center" class="g" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important">
         <tr style="border-collapse:collapse">
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" class="z" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr style="border-collapse:collapse">
              <td align="left" style="Margin:0;padding-bottom:25px;padding-right:30px;padding-left:30px;padding-top:15px;background-position:center bottom">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr style="border-collapse:collapse">
                  <td align="center" class="bd bc" style="padding:0;Margin:0;width:540px">
                   <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr style="border-collapse:collapse">
                      <td align="center" style="padding:0;Margin:0;padding-left:10px;padding-top:10px;padding-right:10px"><span class="r" style="border-style:solid;border-color:#3B2495;background:#6aa84f;border-width:0px;display:inline-block;border-radius:30px;width:auto"><a href="https://ganaderia.sinarca.co/authentication/sign-in" target="_blank" class="n" style="mso-style-priority:100 !important;text-decoration:none !important;mso-line-height-rule:exactly;color:#FFFFFF;font-size:20px;padding:12px 40px 13px 40px;display:inline-block;background:#6aa84f;border-radius:30px;font-family:Montserrat, Helvetica, Roboto, Arial, sans-serif;font-weight:normal;font-style:normal;line-height:24px;width:auto;text-align:center;letter-spacing:0;mso-padding-alt:0;mso-border-alt:10px solid #6aa84f">INGRESAR A MI CUENTA</a></span></td>
                     </tr>
                   </table></td>
                 </tr>
                 <tr style="border-collapse:collapse">
                  <td align="center" valign="top" style="padding:0;Margin:0;width:540px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr style="border-collapse:collapse">
                      <td align="center" style="padding:0;Margin:0;padding-top:10px"><p class="v" style="Margin:0;mso-line-height-rule:exactly;font-family:Montserrat, Helvetica, Roboto, Arial, sans-serif;line-height:21px;letter-spacing:0;color:#4A4A4A;font-size:14px"><br></p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" align="center" class="g" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important">
         <tr style="border-collapse:collapse">
          <td align="center" bgcolor="#93c47d" style="padding:0;Margin:0;background-color:#93c47d">
           <table bgcolor="#00000000" align="center" cellpadding="0" cellspacing="0" class="z" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr style="border-collapse:collapse">
              <td align="left" style="padding:0;Margin:0;padding-top:40px;padding-bottom:30px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr style="border-collapse:collapse">
                  <td align="center" valign="top" style="padding:0;Margin:0;width:600px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr style="border-collapse:collapse">
                      <td align="center" class="u" style="padding:0;Margin:0;font-size:0">
                       <table cellpadding="0" cellspacing="0" class="a o" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr style="border-collapse:collapse">
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:10px"><a target="_blank" href="https://www.facebook.com/profile.php?id=61556817386565" style="mso-line-height-rule:exactly;text-decoration:underline;color:#3B2495;font-size:16px"><img title="Facebook" src="https://ffzppoq.stripocdn.email/content/assets/img/social-icons/logo-white/facebook-logo-white.png" alt="Fb" width="32" style="display:block;font-size:16px;border:0;outline:none;text-decoration:none"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:10px"><a target="_blank" href="https://www.youtube.com/@RtaGanadera" style="mso-line-height-rule:exactly;text-decoration:underline;color:#3B2495;font-size:16px"><img title="Youtube" src="https://ffzppoq.stripocdn.email/content/assets/img/social-icons/logo-white/youtube-logo-white.png" alt="Yt" width="32" style="display:block;font-size:16px;border:0;outline:none;text-decoration:none"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:10px"><a target="_blank" href="https://www.instagram.com/rutaganadera/" style="mso-line-height-rule:exactly;text-decoration:underline;color:#3B2495;font-size:16px"><img title="Instagram" src="https://ffzppoq.stripocdn.email/content/assets/img/social-icons/logo-white/instagram-logo-white.png" alt="Ig" width="32" style="display:block;font-size:16px;border:0;outline:none;text-decoration:none"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0"><a target="_blank" href="https://www.linkedin.com/in/ruta-ganadera-sofware-ganadero-a3b239300/" style="mso-line-height-rule:exactly;text-decoration:underline;color:#3B2495;font-size:16px"><img title="Linkedin" src="https://ffzppoq.stripocdn.email/content/assets/img/social-icons/logo-white/linkedin-logo-white.png" alt="In" width="32" style="display:block;font-size:16px;border:0;outline:none;text-decoration:none"></a></td>
                         </tr>
                       </table></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
             <tr style="border-collapse:collapse">
              <td align="left" style="padding:0;Margin:0;padding-right:30px;padding-left:30px;padding-bottom:30px;background-position:center bottom">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr style="border-collapse:collapse">
                  <td align="center" valign="top" style="padding:0;Margin:0;width:540px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr style="border-collapse:collapse">
                      <td align="center" class="x" style="padding:0;Margin:0"><p style="Margin:0;mso-line-height-rule:exactly;font-family:Montserrat, Helvetica, Roboto, Arial, sans-serif;line-height:18px;letter-spacing:0;color:#CCCCCC;font-size:12px"><br></p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" align="center" class="g" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important">
         <tr style="border-collapse:collapse">
          <td align="center" style="padding:0;Margin:0">
           <table cellspacing="0" cellpadding="0" align="center" class="z" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr style="border-collapse:collapse">
              <td align="left" style="Margin:0;padding-right:20px;padding-left:20px;padding-bottom:30px;padding-top:30px">
               <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr style="border-collapse:collapse">
                  <td valign="top" align="center" style="padding:0;Margin:0;width:560px">
                   <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr style="border-collapse:collapse">
                      <td align="center" style="padding:0;Margin:0;display:none"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table></td>
     </tr>
   </table>
  </div>
 </body>
</html>
    
    
    """
    mensaje = mensaje.replace('{{NotificacionesCorreo}}', Notificacion)

    # Configurar el mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto



    # Agregar el cuerpo del mensaje
    msg.attach(MIMEText(mensaje, 'html'))

    # Establecer conexión con el servidor SMTP
    servidor = smtplib.SMTP(host=servidor_smtp, port=puerto_smtp)
    servidor.starttls()  # Habilitar la capa de seguridad

    # Iniciar sesión en el servidor SMTP
    servidor.login(remitente, password)

    # Enviar el correo electrónico
    servidor.sendmail(remitente, destinatario, msg.as_string())

    # Cerrar la conexión
    servidor.quit()


