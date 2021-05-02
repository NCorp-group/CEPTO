using System;

namespace CeptoApi.Models
{
    public class EventSchema
    {
        public Guid visit_id { get; set; }
        public String event_type { get; set; }
        public DateTime time { get; set; }
        public DateTime time_since_last { get; set; }
    }
}