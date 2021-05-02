using System;
using System.Collections.Generic;

namespace CeptoApi.Models
{
    public class FetchEventsReply
    {
        public String cmd_echo { get; set; }
        public String error_code { get; set; }
        public List<EventSchema> events { get; set; }
    }
}