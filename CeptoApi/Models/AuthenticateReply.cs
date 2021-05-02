using System;

namespace CeptoApi.Models
{
    public class AuthenticateReply
    {
        public String cmd_echo { get; set; }
        public String error_code { get; set; }
        public Guid session_token { get; set; }
        public DateTime expiry { get; set; }
    }
}