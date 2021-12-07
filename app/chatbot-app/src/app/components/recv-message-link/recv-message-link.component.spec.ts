import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecvMessageLinkComponent } from './recv-message-link.component';

describe('RecvMessageLinkComponent', () => {
  let component: RecvMessageLinkComponent;
  let fixture: ComponentFixture<RecvMessageLinkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecvMessageLinkComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RecvMessageLinkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
