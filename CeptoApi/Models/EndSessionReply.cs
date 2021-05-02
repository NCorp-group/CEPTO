using System;

namespace CeptoApi.Models
{
    public class EndSessionReply
    {
        public String cmd_echo { get; set; }
        public String error_code { get; set; }
        public bool success { get; set; }
    }
}