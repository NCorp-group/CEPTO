using System;

namespace CeptoApi.Models
{
    public class EventSchema
    {
        public Guid visit_id { get; set; }
        public String event_type { get; set; }
        public DateTime expiry { get; set; }
        public TimeSpan time_since_last { get; set; }
    }
}